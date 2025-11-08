import sys
from collections import defaultdict
from typing import Dict, Set, List, Tuple, Any

# Tipos para claridad
ProfMateria = Tuple[int, int]
StudentEnrollments = Dict[int, Set[int]]
ProfHoursRequired = Dict[ProfMateria, int]
ClassTuple = Tuple[int, int, int, int] # prof, materia, start, end
Schedule = Dict[int, List[ClassTuple]]

def parse_input(file_path: str) -> Tuple[int, ProfHoursRequired, StudentEnrollments]:
    """Lee el fichero de entrada y extrae los datos del problema."""
    prof_hours_required: ProfHoursRequired = {}
    student_enrollments: StudentEnrollments = {}
    
    with open(file_path, 'r') as f:
        # 1. Número de días
        num_days = int(f.readline().strip())
        
        # 2. Combinaciones Profesor-Materia
        p = int(f.readline().strip())
        for _ in range(p):
            line = f.readline().strip()
            if not line: continue
            prof, materia, hours = map(int, line.split())
            prof_hours_required[(prof, materia)] = hours
            
        # 3. Alumnos y matrículas
        line = f.readline().strip()
        a, m = map(int, line.split())
        for _ in range(a):
            line = f.readline().strip()
            if not line: continue
            parts = list(map(int, line.split()))
            student_id = parts[0]
            materias = set(parts[1:])
            student_enrollments[student_id] = materias
            
    return num_days, prof_hours_required, student_enrollments

# --- PARSE_OUTPUT (MODIFICADO) ---
def parse_output(file: str) -> Tuple[Schedule, List[str]]:
    """
    Lee el fichero de salida (la solución) y lo estructura.
    Devuelve el horario y una lista de errores de formato.
    Si hay errores de formato, para inmediatamente.
    """
    schedule: Schedule = {}
    format_errors: List[str] = []
    
    lines = file.split('\n') 
        
    i = 0
    # MODIFICACION: Inicializar a -1 para permitir que el día 0 sea el primero.
    last_day = -1 
    
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        
        # 1. Parsear el 'header' del día
        try:
            parts = line.split()
            if len(parts) != 2:
                raise ValueError(f"La linea de cabecera de dia debe tener 2 valores (Dia, N_Clases), encontrados: {len(parts)}")
            day, n_classes = int(parts[0]), int(parts[1])
        except (IndexError, ValueError) as e:
            format_errors.append(f"Error Formato: Linea de cabecera mal formada '{line}'. Error: {e}")
            return schedule, format_errors

        # 2. Comprobar orden de días
        if day <= last_day:
            format_errors.append(f"Error Formato: Dia {day} aparece fuera de orden (despues de {last_day}).")
            return schedule, format_errors
            
        last_day = day
        schedule[day] = []
        
        # 3. Preparar lectura de clases
        class_lines_start = i + 1
        class_lines_end = i + 1 + n_classes
        
        if class_lines_end > len(lines):
            format_errors.append(f"Error Formato: Dia {day} dice tener {n_classes} clases, pero el fichero acaba.")
            return schedule, format_errors
            
        # 4. Parsear las N clases
        for j in range(class_lines_start, class_lines_end):
            class_line = lines[j].strip()
            try:
                class_parts = class_line.split()
                if len(class_parts) != 4:
                    raise ValueError(f"Una linea de clase debe tener 4 valores, encontrados: {len(class_parts)}")
                prof, materia, start, end = map(int, class_parts)
                schedule[day].append((prof, materia, start, end))
                
            except (IndexError, ValueError) as e:
                format_errors.append(f"Error Formato: Dia {day}, linea de clase mal formada '{class_line}'. Error: {e}")
                return schedule, format_errors
        
        i = class_lines_end
            
    return schedule, format_errors

def _validate_prof_hours(schedule: Schedule) -> Tuple[bool, List[str], Dict[ProfMateria, int]]:
    """Función helper para validar reglas de profesores y contar horas."""
    errors: List[str] = []
    prof_hours_taught: Dict[ProfMateria, int] = defaultdict(int)
    prof_daily_schedule: Dict[int, Dict[int, List[Tuple[int, int]]]] = defaultdict(lambda: defaultdict(list))

    # 1. Recopilar todas las clases
    for day, classes in schedule.items():
        for prof, materia, start, end in classes:
            
            if start >= end:
                 errors.append(f"Error Duracion: Dia {day}, Profesor {prof} tiene clase con duracion <= 0: ({start}, {end}).")
                 continue 
            
            duration = end - start
            prof_hours_taught[(prof, materia)] += duration
            prof_daily_schedule[prof][day].append((start, end))

    # 2. Validar Regla 3 (Continuidad y Solapamiento)
    for prof, days_data in prof_daily_schedule.items():
        for day, classes in days_data.items():
            if not classes:
                continue
            
            classes.sort(key=lambda x: x[0]) 
            
            for k in range(len(classes) - 1):
                if classes[k][1] > classes[k+1][0]:
                    errors.append(f"Error Regla 3 (Solapamiento): Dia {day}, Profesor {prof} tiene clases solapadas: {classes[k]} y {classes[k+1]}.")
            
            if not classes:
                continue
                
            current_stretch = 0
            last_end = -1
            
            for start, end in classes:
                duration = end - start
                
                if start == last_end: 
                    current_stretch += duration
                else: 
                    current_stretch = duration
                
                if current_stretch > 3:
                    errors.append(f"Error Regla 3 (3h+): Dia {day}, Profesor {prof} imparte > 3 horas seguidas (bloque termina a las {end}).")

                last_end = end

    if errors:
        return False, errors, prof_hours_taught
    
    return True, [], prof_hours_taught

# --- VALIDATE_SCHEDULE (MODIFICADO) ---
def validate_schedule(
    num_days: int, 
    prof_hours_required: ProfHoursRequired, 
    schedule: Schedule
) -> List[str]:
    """
    Valida el horario completo contra todas las reglas del problema.
    Muestra *todos* los errores de reglas, incluso si son derivados.
    """
    errors: List[str] = []
    
    # --- INICIO MODIFICACION REGLA 4 ---
    # Regla 4: Detectar si se usa indexación 0 o 1
    found_days = set(schedule.keys())
    
    expected_days: Set[int]
    expected_range_str: str
    
    if 0 in found_days:
        # Si el Día 0 existe, asumimos indexación 0 (0 a num_days-1)
        expected_days = set(range(0, num_days))
        expected_range_str = f"0 a {num_days - 1}"
    else:
        # Si no, asumimos indexación 1 (1 a num_days)
        # Esto también cubre el caso de un schedule vacío
        expected_days = set(range(1, num_days + 1))
        expected_range_str = f"1 a {num_days}"

    missing_days = expected_days - found_days
    for d in sorted(list(missing_days)):
        errors.append(f"Error Regla 4: El dia {d} falta en el fichero de salida (esperados: {expected_range_str}).")
        
    extra_days = found_days - expected_days
    for d in sorted(list(extra_days)):
        errors.append(f"Error Regla 4: El dia {d} aparece en la salida, pero no es valido (esperados: {expected_range_str}).")
    # --- FIN MODIFICACION REGLA 4 ---

    # Validar reglas de profesores (Regla 3) y contar horas (Regla 1)
    valid_prof, prof_errors, prof_hours_taught = _validate_prof_hours(schedule)
    if not valid_prof:
        errors.extend(prof_errors)

    # Reglas de horario (Regla 5) y solapamiento de materias (Regla 2)
    for day, classes in schedule.items():
        # Ignorar la validación de reglas para días que ya reportamos como "extra"
        if day in extra_days:
            continue
            
        materia_slots: Dict[int, List[Tuple[int, int]]] = defaultdict(list)
        
        for prof, materia, start, end in classes:
            # Regla 5: Horario 8:00 - 20:00
            if not (start >= 8 and end <= 20):
                errors.append(f"Error Regla 5: Dia {day}, Clase ({prof}, {materia}) esta fuera de horario: [{start}, {end}). Valido: [8, 20).")
            
            # Comprobar solapamiento de esta materia (Regla 2)
            if start < end: # Solo comprobar si la duración es positiva
                for existing_start, existing_end in materia_slots[materia]:
                    if max(start, existing_start) < min(end, existing_end):
                        errors.append(f"Error Regla 2: Dia {day}, Materia {materia} se imparte simultaneamente. Conflicto entre [{start}, {end}) y [{existing_start}, {existing_end}).")
                materia_slots[materia].append((start, end))

    # Regla 1: Todos los profesores imparten sus horas
    for (prof, materia), hours_req in prof_hours_required.items():
        hours_taught = prof_hours_taught.get((prof, materia), 0)
        if hours_taught != hours_req:
            errors.append(f"Error Regla 1: Profesor {prof}, Materia {materia} - Horas requeridas: {hours_req}, Horas impartidas: {hours_taught}.")
            
    # Comprobar si se han impartido horas no asignadas
    for (prof, materia), hours_taught in prof_hours_taught.items():
        if (prof, materia) not in prof_hours_required and hours_taught > 0:
            errors.append(f"Error Extra: Profesor {prof}, Materia {materia} imparte {hours_taught}h, pero no estaba en la entrada.")

    return errors

def calculate_score(student_enrollments: StudentEnrollments, schedule: Schedule) -> int:
    """
    Calcula la puntuación total basada en las horas de asistencia de los alumnos.
    """
    total_score = 0
    
    for student_id, enrolled_materias in student_enrollments.items():
        student_total_hours = 0
        
        for day in sorted(schedule.keys()):
            classes_today = schedule.get(day, [])
            
            available_classes = []
            for prof, materia, start, end in classes_today:
                if materia in enrolled_materias and start < end:
                    duration = end - start
                    available_classes.append((start, -duration, end))
            
            if not available_classes:
                continue
                
            available_classes.sort()
            
            student_day_hours = 0
            last_class_end_time = 0 
            
            i = 0
            while i < len(available_classes):
                current_start_time = available_classes[i][0]
                
                if current_start_time < last_class_end_time:
                    i += 1
                    continue
                
                choices_at_this_time = []
                while i < len(available_classes) and available_classes[i][0] == current_start_time:
                    choices_at_this_time.append(available_classes[i])
                    i += 1
                
                chosen_class = choices_at_this_time[0]
                start, neg_duration, end = chosen_class
                duration = -neg_duration
                
                student_day_hours += duration
                last_class_end_time = end
            
            student_total_hours += student_day_hours
            
        total_score += student_total_hours
        
    return total_score

def calculate_theoretical_max(
    prof_hours_required: ProfHoursRequired, 
    student_enrollments: StudentEnrollments
) -> int:
    """
    Calcula la puntuación máxima teórica posible para esta entrada.
    """
    total_hours_per_materia: Dict[int, int] = defaultdict(int)
    for (prof, materia), hours in prof_hours_required.items():
        total_hours_per_materia[materia] += hours
        
    students_per_materia: Dict[int, int] = defaultdict(int)
    for student_id, enrolled_materias in student_enrollments.items():
        for materia in enrolled_materias:
            students_per_materia[materia] += 1
            
    theoretical_max_score = 0
    for materia, total_hours in total_hours_per_materia.items():
        num_students = students_per_materia.get(materia, 0)
        theoretical_max_score += total_hours * num_students
        
    return theoretical_max_score


def main():
    """Función principal del validador."""
    
    INPUT_FILE = "entrada.txt"
    OUTPUT_FILE = "salida.txt"
    
    print(f"--- Iniciando Validacion ---")
    print(f"Fichero de Entrada: {INPUT_FILE}")
    print(f"Fichero de Salida:  {OUTPUT_FILE}")
    print("---------------------------------")
    
    try:
        num_days, prof_hours, student_enrollments = parse_input(INPUT_FILE)
    except FileNotFoundError:
        print(f"Error Critico: No se encuentra el fichero de entrada '{INPUT_FILE}'.")
        return
    except Exception as e:
        print(f"Error Critico al parsear ENTRADA: {e}")
        return

    try:
        schedule, format_errors = parse_output(OUTPUT_FILE)
    except FileNotFoundError:
        print(f"Error Critico: No se encuentra el fichero de salida '{OUTPUT_FILE}'.")
        return
    except Exception as e:
        print(f"Error Critico al parsear SALIDA: {e}")
        return

    if format_errors:
        print("Error de Formato en Fichero de Salida:")
        for err in format_errors:
            print(f"  - {err}")
        print("Validacion cancelada por errores de formato.")
        return

    print("Validando reglas del problema...")
    validation_errors = validate_schedule(num_days, prof_hours, schedule)
    
    if validation_errors:
        print("Validacion FALLIDA. Se encontraron los siguientes errores:")
        unique_errors = sorted(list(set(validation_errors)))
        for i, err in enumerate(unique_errors, 1):
            print(f"  {i}. {err}")
        print("---------------------------------")
    else:
        print("Validacion de Reglas: CORRECTA")
        print("---------------------------------")
        
        print("Calculando puntuacion...")
        
        theoretical_max = calculate_theoretical_max(prof_hours, student_enrollments)
        score = calculate_score(student_enrollments, schedule)
        
        if score == theoretical_max:
            print(f"Puntuacion Final: {score} horas")
            print("Maximo alcanzado")
        else:
            print(f"Puntuacion Final: {score} horas (Aun se puede mejorar)")
            
        print("---------------------------------")

if __name__ == "__main__":
    main()
