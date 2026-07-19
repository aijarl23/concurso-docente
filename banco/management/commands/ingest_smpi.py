"""Ingesta de preguntas del Banco Oficial de Ítems (SMPI).

Formato esperado: JSON array con objetos que contienen:
  - titulo (opcional): contexto/situacion
  - contexto: enunciado o parte de la situacion
  - enunciado: pregunta clave
  - opcion_a, opcion_b, opcion_c, opcion_d: alternativas de respuesta
  - respuesta_correcta: A|B|C|D
  - area: codigo de area desde BancoPregunta.AREA_CHOICES
  - competencia: string libre, ej. "Lectura critica" o "Normativa educativa aplicada"
  - dificultad: facil|medio|alto|muy_alto
  - tipo_item: estandar|mas_adecuada|menos_adecuada
  - idoneidad_a, idoneidad_b, idoneidad_c, idoneidad_d (opcional, solo si tipo_item != estandar):
    valores 0-4 indicando calidad de la respuesta
  - justificacion (opcional): explicacion del por que es correcta
  - fuente_normativa (opcional): decreto/ley/documento de referencia
  - proceso_cognitivo (opcional): identificacion|comprension_aplicada|analisis_situacional|evaluacion_juicio
  - puntaje_validacion (opcional): 0-100 score de calidad del item

Flujo:
  1. Carga JSON desde archivo o stdin
  2. Deduplica por similitud textual (Jaccard >= 0.92 en enunciado)
  3. Normaliza valores de choices (area, dificultad, tipo_item)
  4. Inserta en BancoPregunta con estado='importado_smpi'
  5. Reporta duplicados, errores, y totales ingresados

Uso:
  python manage.py ingest_smpi questions.json
  cat questions.json | python manage.py ingest_smpi --stdin
"""

import json
import sys
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from banco.models import BancoPregunta, Categoria
from dashboard.question_generator import normalize, token_set, jaccard


class Command(BaseCommand):
    help = 'Ingesta de preguntas del Banco Oficial de Ítems (SMPI)'

    def add_arguments(self, parser):
        parser.add_argument(
            'archivo',
            nargs='?',
            type=str,
            help='Ruta al archivo JSON con preguntas'
        )
        parser.add_argument(
            '--stdin',
            action='store_true',
            help='Leer JSON desde stdin en lugar de archivo'
        )
        parser.add_argument(
            '--categoria',
            type=str,
            default='Banco Oficial SMPI',
            help='Nombre de la categoría para agrupar preguntas importadas'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Validar sin insertar nada en la BD'
        )
        parser.add_argument(
            '--threshold',
            type=float,
            default=0.92,
            help='Umbral de similitud Jaccard para detectar duplicados (0-1)'
        )

    def handle(self, *args, **options):
        archivo = options['archivo']
        usar_stdin = options['stdin']
        categoria_nombre = options['categoria']
        dry_run = options['dry_run']
        threshold = options['threshold']

        if usar_stdin:
            contenido = sys.stdin.read()
            try:
                preguntas = json.loads(contenido)
            except json.JSONDecodeError as e:
                raise CommandError(f'JSON inválido en stdin: {e}')
        elif archivo:
            try:
                with open(archivo, 'r', encoding='utf-8') as f:
                    preguntas = json.load(f)
            except FileNotFoundError:
                raise CommandError(f'Archivo no encontrado: {archivo}')
            except json.JSONDecodeError as e:
                raise CommandError(f'JSON inválido en {archivo}: {e}')
        else:
            raise CommandError('Especifica archivo o usa --stdin')

        if not isinstance(preguntas, list):
            raise CommandError('JSON debe ser un array de preguntas')

        self.stdout.write(f'Cargadas {len(preguntas)} preguntas para ingesta')

        categoria, _ = Categoria.objects.get_or_create(nombre=categoria_nombre)
        self.stdout.write(f'Categoría: {categoria.nombre}')

        validadas = []
        errores = []
        duplicadas = []

        for idx, preg in enumerate(preguntas, 1):
            try:
                validada = self._validar_pregunta(preg, idx)
                validadas.append(validada)
            except ValueError as e:
                errores.append((idx, str(e)))

        self.stdout.write(f'Validadas: {len(validadas)}, Errores: {len(errores)}')

        for idx, error in errores[:5]:
            self.stdout.write(self.style.WARNING(f'  Pregunta {idx}: {error}'))
        if len(errores) > 5:
            self.stdout.write(self.style.WARNING(f'  ... y {len(errores) - 5} más'))

        duplicadas = self._detectar_duplicados(validadas, threshold)
        unicas = [v for v in validadas if v not in duplicadas]
        self.stdout.write(f'Únicas (no duplicadas): {len(unicas)}')
        if duplicadas:
            self.stdout.write(self.style.WARNING(f'  Duplicados detectados: {len(duplicadas)}'))

        if not dry_run and unicas:
            with transaction.atomic():
                insertadas = self._insertar_preguntas(unicas, categoria)
            self.stdout.write(self.style.SUCCESS(f'[OK] Insertadas {insertadas} preguntas'))
        elif dry_run:
            self.stdout.write(f'[DRY RUN] Se insertarían {len(unicas)} preguntas')

    def _validar_pregunta(self, preg, idx):
        """Valida estructura y normaliza valores de una pregunta."""
        errores = []

        contexto = (preg.get('titulo') or '') + '\n' + (preg.get('contexto') or '')
        contexto = contexto.strip()
        if not contexto:
            errores.append('contexto/titulo requeridos')

        enunciado = preg.get('enunciado', '').strip()
        if not enunciado:
            errores.append('enunciado requerido')

        for opcion in ['A', 'B', 'C', 'D']:
            if not preg.get(f'opcion_{opcion.lower()}', '').strip():
                errores.append(f'opcion_{opcion.lower()} requerida')

        respuesta = preg.get('respuesta_correcta', '').upper()
        if respuesta not in ['A', 'B', 'C', 'D']:
            errores.append('respuesta_correcta debe ser A|B|C|D')

        area = preg.get('area', 'general').lower()
        area_validas = {choice[0] for choice in BancoPregunta.AREA_CHOICES}
        if area not in area_validas:
            errores.append(f'area inválida: {area}. Válidas: {area_validas}')

        dificultad = preg.get('dificultad', 'alto').lower()
        dif_validas = {choice[0] for choice in BancoPregunta.DIFICULTAD_CHOICES}
        if dificultad not in dif_validas:
            errores.append(f'dificultad inválida: {dificultad}. Válidas: {dif_validas}')

        tipo_item = preg.get('tipo_item', 'estandar').lower()
        tipo_validas = {choice[0] for choice in BancoPregunta.TIPO_ITEM_CHOICES}
        if tipo_item not in tipo_validas:
            errores.append(f'tipo_item inválido: {tipo_item}. Válidas: {tipo_validas}')

        if errores:
            raise ValueError('; '.join(errores))

        idoneidad = {}
        if tipo_item != 'estandar':
            for opcion in ['A', 'B', 'C', 'D']:
                val = preg.get(f'idoneidad_{opcion.lower()}')
                if val is not None:
                    if not isinstance(val, int) or not 0 <= val <= 4:
                        raise ValueError(f'idoneidad_{opcion.lower()} debe ser 0-4')
                    idoneidad[opcion.lower()] = val

        proceso_cognitivo = preg.get('proceso_cognitivo', '').lower()
        proc_validas = {choice[0] for choice in BancoPregunta.PROCESO_COGNITIVO_CHOICES}
        if proceso_cognitivo and proceso_cognitivo not in proc_validas:
            raise ValueError(f'proceso_cognitivo inválido: {proceso_cognitivo}')

        return {
            'contexto': contexto,
            'enunciado': enunciado,
            'opcion_a': preg.get('opcion_a', '').strip(),
            'opcion_b': preg.get('opcion_b', '').strip(),
            'opcion_c': preg.get('opcion_c', '').strip(),
            'opcion_d': preg.get('opcion_d', '').strip(),
            'respuesta_correcta': respuesta,
            'area': area,
            'competencia': preg.get('competencia', '').strip(),
            'dificultad': dificultad,
            'nivel_dificultad': dificultad,
            'tipo_item': tipo_item,
            'idoneidad': idoneidad,
            'justificacion': preg.get('justificacion', '').strip(),
            'fuente_normativa': preg.get('fuente_normativa', '').strip(),
            'proceso_cognitivo': proceso_cognitivo,
            'puntaje_validacion': preg.get('puntaje_validacion'),
        }

    def _detectar_duplicados(self, validadas, threshold):
        """Identifica preguntas duplicadas por similitud de enunciado."""
        duplicadas = []
        enunciados_vistos = {}

        for preg in validadas:
            enun = preg['enunciado']
            tokens_actual = token_set(enun)

            for enun_prev, similitud in enunciados_vistos.items():
                tokens_prev = token_set(enun_prev)
                sim = jaccard(tokens_actual, tokens_prev)
                if sim >= threshold:
                    duplicadas.append(preg)
                    break
            else:
                enunciados_vistos[enun] = True

        return duplicadas

    def _insertar_preguntas(self, validadas, categoria):
        """Inserta preguntas en la BD."""
        insertadas = 0

        for preg_data in validadas:
            pregunta = BancoPregunta(
                categoria=categoria,
                contexto=preg_data['contexto'],
                enunciado=preg_data['enunciado'],
                opcion_a=preg_data['opcion_a'],
                opcion_b=preg_data['opcion_b'],
                opcion_c=preg_data['opcion_c'],
                opcion_d=preg_data['opcion_d'],
                respuesta_correcta=preg_data['respuesta_correcta'],
                area=preg_data['area'],
                competencia=preg_data['competencia'],
                dificultad=preg_data['dificultad'],
                nivel_dificultad=preg_data['nivel_dificultad'],
                tipo_item=preg_data['tipo_item'],
                justificacion=preg_data['justificacion'],
                fuente_normativa=preg_data['fuente_normativa'],
                proceso_cognitivo=preg_data['proceso_cognitivo'],
                puntaje_validacion=preg_data['puntaje_validacion'],
                estado='publicado',
                autor='SMPI',
                es_premium=False,
            )

            if preg_data['idoneidad']:
                for letra, valor in preg_data['idoneidad'].items():
                    setattr(pregunta, f'idoneidad_{letra}', valor)

            pregunta.save()
            insertadas += 1

        return insertadas
