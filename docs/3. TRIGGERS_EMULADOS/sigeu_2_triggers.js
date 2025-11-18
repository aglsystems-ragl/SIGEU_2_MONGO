//D:\SIGEU\SIGEU_2_MONGO\docs
// -----------------------------------------------------
// SIGEU_2 – EMULACION DE "Triggers" EN MONGO DB
// 
// Este archivo NO se ejecuta solo. Puies define funciones
// que luego se llaman desde Compass o desde la API.
// -----------------------------------------------------
// Este archivo debe cargarse en mongosh con:
//
//   use('sigeu_2')
//   load("D:\\SIGEU\\SIGEU_2_MONGO\\docs\\sigeu_2_triggers.js")
//
// Después de cargarlo, se puede usar:
//
//   crearUsuario(...)
//   asignarUsuarioAPrograma(...)
//   registrarOrganizadorEvento(...)
//   evaluarEvento({...})
// -----------------------------------------------------

// =====================================================
//  SIGEU_2 - TRIGGERS LÓGICOS PARA MONGODB
//  Archivo completo y funcional
// =====================================================

use('sigeu_2');

// =====================================================
//  HELPERS
// =====================================================

// Obtener usuario o lanzar error
function getUsuarioOrFail(usuarioId) {
  const usuario = db.usuario.findOne({ _id: usuarioId });
  if (!usuario) {
    throw new Error(`Usuario ${usuarioId} no existe`);
  }
  return usuario;
}

// =====================================================
// 1. crearUsuario()
// =====================================================
function crearUsuario(nombre, apellido, correo, rol) {

  // Validar dominio uao.edu.co
  const regex = /^[a-z0-9._%+-]+@uao\.edu\.co$/i;
  if (!regex.test(correo)) {
    throw new Error('El correo debe ser del dominio @uao.edu.co');
  }

  // Validar rol permitido
  if (!['docente','estudiante','secretario'].includes(rol)) {
    throw new Error('Rol inválido. Debe ser docente, estudiante o secretario.');
  }

  const res = db.usuario.insertOne({
    nombre, apellido, correo, rol
  });

  return res.insertedId;
}

// =====================================================
// 2. asignarUsuarioAPrograma()
// =====================================================
function asignarUsuarioAPrograma(programaId, usuarioId) {

  const usuario = getUsuarioOrFail(usuarioId);

  if (usuario.rol !== 'estudiante') {
    throw new Error('Solo usuarios con rol estudiante pueden pertenecer a un programa académico');
  }

  db.programa_usuario.insertOne({
    programa_id: programaId,
    usuario_id: usuarioId
  });
}

// =====================================================
// 3. registrarOrganizadorEvento()
// =====================================================
function registrarOrganizadorEvento(usuarioId, eventoId) {

  const usuario = getUsuarioOrFail(usuarioId);

  if (!['docente', 'estudiante'].includes(usuario.rol)) {
    throw new Error('Solo docentes o estudiantes pueden ser organizadores de eventos');
  }

  db.usuario_organizador.insertOne({
    usuario_id: usuarioId,
    evento_id: eventoId
  });
}

// =====================================================
// 4. evaluarEvento()
// =====================================================
function evaluarEvento({ eventoId, usuarioEvaluadorId, estado, justificacion, actaPdfUrl }) {

  if (!['aprobado','rechazado'].includes(estado)) {
    throw new Error('Estado inválido. Use aprobado o rechazado.');
  }

  const evaluador = getUsuarioOrFail(usuarioEvaluadorId);

  if (evaluador.rol !== 'secretario') {
    throw new Error('Solo usuarios con rol secretario pueden evaluar eventos');
  }

  const evento = db.evento.findOne({ _id: eventoId });
  if (!evento) {
    throw new Error(`Evento ${eventoId} no existe`);
  }

  // Validar que el secretario pertenece a la facultad del evento
  const coincide = db.facultad_usuario.findOne({
    facultad_id: evento.facultad_id,
    usuario_id: usuarioEvaluadorId
  });

  if (!coincide) {
    throw new Error('El secretario NO pertenece a la facultad del evento');
  }

  // Insertar evaluación
  db.evaluacion_evento.insertOne({
    justificacion,
    acta_pdf_url: actaPdfUrl,
    fecha_evaluacion: new Date(),
    estado,
    evento_id: eventoId,
    usuario_id: usuarioEvaluadorId
  });

  // Actualizar estado del evento
  db.evento.updateOne(
    { _id: eventoId },
    { $set: { estado: estado } }
  );
}

print("TRIGGERS SIGEU_2 cargados correctamente.");
