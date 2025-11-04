import bpy
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Nombre de la cámara (ajusta si tu cámara tiene otro nombre)
camera_name = "Camera2"

logger.info(f"Buscando cámara: {camera_name}")

# Obtener la cámara
camera = bpy.data.objects.get(camera_name)

if camera is None:
    logger.error(f"No se encontró la cámara '{camera_name}'")
    available_cameras = [obj.name for obj in bpy.data.objects if obj.type == 'CAMERA']
    logger.info(f"Cámaras disponibles: {available_cameras}")
    exit(1)
else:
    logger.info(f"Cámara encontrada: {camera.name} (tipo: {camera.type})")

    # Seleccionar la cámara y asegurarse de que esté activa
    bpy.context.view_layer.objects.active = camera
    camera.select_set(True)
    logger.info(f"Cámara seleccionada: {camera.name}")

    # Crear keyframes en las propiedades que queremos animar (necesario para F-Curves)
    frame_start = 1
    camera.keyframe_insert(data_path="location", frame=frame_start)
    camera.keyframe_insert(data_path="rotation_euler", frame=frame_start)
    logger.info(f"Keyframes iniciales creados en frame {frame_start}")

    # Verificar que se crearon las animation data y action
    if camera.animation_data is None or camera.animation_data.action is None:
        logger.error("No se pudieron crear los datos de animación")
        print("Exiting because no camera was found.")

    logger.info(f"Action creada: {camera.animation_data.action.name}")

    # Obtener las F-Curves creadas
    fcurves = camera.animation_data.action.fcurves
    logger.info(f"F-Curves disponibles: {len(fcurves)}")

    # Mapeo de data_path y array_index a configuración de noise
    noise_configs = [
        ("location", 0, 0.05, 1.0, 0.0, "Location X"),
        ("location", 1, 0.05, 1.2, 2.5, "Location Y"),
        ("location", 2, 0.03, 0.8, 5.0, "Location Z"),
        ("rotation_euler", 0, 0.02, 1.5, 7.5, "Rotation X"),
        ("rotation_euler", 1, 0.02, 1.5, 10.0, "Rotation Y"),
        ("rotation_euler", 2, 0.02, 1.5, 12.5, "Rotation Z"),
    ]

    # Agregar modificador de noise a cada F-Curve
    for data_path, array_index, strength, scale, phase, description in noise_configs:
        logger.info(f"Procesando {description} ({data_path}[{array_index}])")

        # Buscar la F-Curve correspondiente
        fcurve = None
        for fc in fcurves:
            if fc.data_path == data_path and fc.array_index == array_index:
                fcurve = fc
                break

        if fcurve is None:
            logger.warning(f"No se encontró F-Curve para {description}, creando keyframe...")
            camera.keyframe_insert(data_path=data_path, index=array_index, frame=frame_start)
            for fc in fcurves:
                if fc.data_path == data_path and fc.array_index == array_index:
                    fcurve = fc
                    break

        if fcurve:
            # Agregar el modificador de noise usando bpy.ops
            # Primero seleccionar la F-Curve en el contexto
            for area in bpy.context.screen.areas:
                if area.type == 'GRAPH_EDITOR':
                    logger.warning("Se necesita el Graph Editor abierto para usar bpy.ops.graph")
                    break

            # Método alternativo: agregar directamente al fcurve
            noise_mod = fcurve.modifiers.new(type='NOISE')
            noise_mod.strength = strength
            noise_mod.scale = scale
            noise_mod.phase = phase
            noise_mod.depth = 1

            logger.info(f"✓ Noise agregado a {description}: strength={strength}, scale={scale}, phase={phase}")
        else:
            logger.error(f"✗ No se pudo crear F-Curve para {description}")

    logger.info(f"✓ Modificadores de Noise (F-Curve) agregados exitosamente a '{camera_name}'")
    logger.info("Puedes ajustar los valores en el Graph Editor")