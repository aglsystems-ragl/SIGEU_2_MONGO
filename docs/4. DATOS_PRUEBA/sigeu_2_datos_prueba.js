
// SIGEU_2 – Datos de prueba
// SE EJECUTA DESPUES DEL ARCHIVO sigeu_2_triggers.js
// Ejecutar en mongosh con:
//
//   use('sigeu_2')
//   load("D:\\SIGEU\\SIGEU_2_MONGO\\docs\\sigeu_2_datos_prueba.js")
//
// Requiere que previamente se haya cargado
// sigeu_2_triggers.js (porque usa crearUsuario, etc.)
// -----------------------------------------------------


use('sigeu_2');

// =====================================================
//  LIMPIAR COLECCIONES
// =====================================================

db.evento.deleteMany({});
db.usuario.deleteMany({});
db.contrasena.deleteMany({});
db.programa_usuario.deleteMany({});
db.unidad_usuario.deleteMany({});
db.facultad_usuario.deleteMany({});
db.usuario_organizador.deleteMany({});
db.lugar_evento.deleteMany({});
db.organizacion_externa.deleteMany({});
db.participa.deleteMany({});
db.evaluacion_evento.deleteMany({});

db.facultad.deleteMany({});
db.unidad_academica.deleteMany({});
db.programa_academico.deleteMany({});
db.lugar.deleteMany({});

// =====================================================
//  1. FACULTAD
// =====================================================

const facIngId = db.facultad.insertOne({
  nombre: "Facultad de Ingeniería",
  telefono: "6023456789"
}).insertedId;

const facEcoId = db.facultad.insertOne({
  nombre: "Facultad de Ciencias Económicas",
  telefono: "6029876543"
}).insertedId;

// =====================================================
//  2. UNIDAD ACADEMICA
// =====================================================

const uaSisId = db.unidad_academica.insertOne({
  nombre: "Unidad Académica Ingeniería de Sistemas",
  facultad_id: facIngId
}).insertedId;

const uaIndId = db.unidad_academica.insertOne({
  nombre: "Unidad Académica Ingeniería Industrial",
  facultad_id: facIngId
}).insertedId;

const uaAdmId = db.unidad_academica.insertOne({
  nombre: "Unidad Académica Administración de Empresas",
  facultad_id: facEcoId
}).insertedId;

// =====================================================
//  3. PROGRAMAS
// =====================================================

const progSisId = db.programa_academico.insertOne({
  nombre: "Ingeniería de Sistemas",
  facultad_id: facIngId
}).insertedId;

const progIndId = db.programa_academico.insertOne({
  nombre: "Ingeniería Industrial",
  facultad_id: facIngId
}).insertedId;

const progAdmId = db.programa_academico.insertOne({
  nombre: "Administración de Empresas",
  facultad_id: facEcoId
}).insertedId;

const progConId = db.programa_academico.insertOne({
  nombre: "Contaduría Pública",
  facultad_id: facEcoId
}).insertedId;

// =====================================================
//  4. USUARIOS
// =====================================================

function cu(nom, ape, alias, rol) {
  return crearUsuario(nom, ape, alias.toLowerCase() + "@uao.edu.co", rol);
}

// 10 Estudiantes
const uEst1  = cu("Pedro","Pérez","pedro.perez","estudiante");
const uEst2  = cu("Ana","Gómez","ana.gomez","estudiante");
const uEst3  = cu("Luis","Rodríguez","luis.rodriguez","estudiante");
const uEst4  = cu("María","Lozano","maria.lozano","estudiante");
const uEst5  = cu("Juan","Castro","juan.castro","estudiante");
const uEst6  = cu("Laura","Mina","laura.mina","estudiante");
const uEst7  = cu("Carlos","Rivas","carlos.rivas","estudiante");
const uEst8  = cu("Diana","Murillo","diana.murillo","estudiante");
const uEst9  = cu("Andrés","Ramírez","andres.ramirez","estudiante");
const uEst10 = cu("Paola","Quintero","paola.quintero","estudiante");

// 5 Docentes
const uDoc1 = cu("Julián","Zapata","julian.zapata","docente");
const uDoc2 = cu("Gloria","Patiño","gloria.patino","docente");
const uDoc3 = cu("Martha","López","martha.lopez","docente");
const uDoc4 = cu("Ricardo","Arias","ricardo.arias","docente");
const uDoc5 = cu("Helena","Ortiz","helena.ortiz","docente");

// 4 Secretarios
const uSec1 = cu("Fernando","Ríos","fernando.rios","secretario");
const uSec2 = cu("Camilo","Gallego","camilo.gallego","secretario");
const uSec3 = cu("Sara","Beltrán","sara.beltran","secretario");
const uSec4 = cu("Viviana","Ruiz","viviana.ruiz","secretario");

// =====================================================
//  5. CONTRASEÑAS
// =====================================================

db.contrasena.insertMany([
  { usuario_id: uSec1, clave: "clave123", fecha_creacion: new Date(), vigente: true },
  { usuario_id: uSec2, clave: "clave456", fecha_creacion: new Date(), vigente: true }
]);

// =====================================================
//  6. ASIGNAR ESTUDIANTES A PROGRAMAS
// =====================================================

asignarUsuarioAPrograma(progSisId, uEst1);
asignarUsuarioAPrograma(progSisId, uEst2);
asignarUsuarioAPrograma(progIndId, uEst3);
asignarUsuarioAPrograma(progIndId, uEst4);
asignarUsuarioAPrograma(progAdmId, uEst5);
asignarUsuarioAPrograma(progAdmId, uEst6);
asignarUsuarioAPrograma(progConId, uEst7);
asignarUsuarioAPrograma(progConId, uEst8);
asignarUsuarioAPrograma(progConId, uEst9);
asignarUsuarioAPrograma(progConId, uEst10);

// =====================================================
//  7. UNIDAD – USUARIO
// =====================================================

db.unidad_usuario.insertMany([
  { unidad_id: uaSisId, usuario_id: uDoc1 },
  { unidad_id: uaIndId, usuario_id: uDoc2 },
  { unidad_id: uaSisId, usuario_id: uDoc3 },
  { unidad_id: uaAdmId, usuario_id: uDoc4 },
  { unidad_id: uaAdmId, usuario_id: uDoc5 },
  { unidad_id: uaSisId, usuario_id: uSec1 },
  { unidad_id: uaIndId, usuario_id: uSec2 },
  { unidad_id: uaAdmId, usuario_id: uSec3 },
  { unidad_id: uaAdmId, usuario_id: uSec4 }
]);

// =====================================================
//  8. FACULTAD – USUARIO
// =====================================================

db.facultad_usuario.insertMany([
  { facultad_id: facIngId, usuario_id: uSec1 },
  { facultad_id: facIngId, usuario_id: uSec2 },
  { facultad_id: facEcoId, usuario_id: uSec3 },
  { facultad_id: facEcoId, usuario_id: uSec4 }
]);

// =====================================================
//  9. LUGARES
// =====================================================

const lug1 = db.lugar.insertOne({
  ubicacion: "Auditorio Central",
  capacidad: 200,
  tipo: "auditorio"
}).insertedId;

const lug2 = db.lugar.insertOne({
  ubicacion: "Sala 201",
  capacidad: 60,
  tipo: "salon"
}).insertedId;

const lug3 = db.lugar.insertOne({
  ubicacion: "Laboratorio de Computo",
  capacidad: 40,
  tipo: "laboratorio"
}).insertedId;

const lug4 = db.lugar.insertOne({
  ubicacion: "Cancha Múltiple",
  capacidad: 150,
  tipo: "cancha"
}).insertedId;

const lug5 = db.lugar.insertOne({
  ubicacion: "Sala de Conferencias",
  capacidad: 80,
  tipo: "salon"
}).insertedId;

// =====================================================
//  10. EVENTOS (aval_pdf_url y aval_tipo NO pueden ser null)
// =====================================================

function hora(h) {
  return new Date(`2025-01-01T${h}:00Z`);
}

const ev1 = db.evento.insertOne({
  nombre_evento: "Seminario IA",
  tipo: "academico",
  descripcion: "Aplicaciones de IA",
  fecha_evento: new Date("2025-03-15"),
  hora_inicio: hora("09:00"),
  hora_fin: hora("12:00"),
  estado: "en_revision",
  aval_pdf_url: "http://example.com/aval1.pdf",
  aval_tipo: "director_programa",
  facultad_id: facIngId
}).insertedId;

const ev2 = db.evento.insertOne({
  nombre_evento: "Hackatón de Datos",
  tipo: "academico",
  descripcion: "Competencia de analítica",
  fecha_evento: new Date("2025-04-10"),
  hora_inicio: hora("08:00"),
  hora_fin: hora("18:00"),
  estado: "registrado",
  aval_pdf_url: "http://example.com/aval2.pdf",
  aval_tipo: "director_docencia",
  facultad_id: facIngId
}).insertedId;

const ev3 = db.evento.insertOne({
  nombre_evento: "Jornada Emprendimiento",
  tipo: "academico",
  descripcion: "Feria de emprendimiento",
  fecha_evento: new Date("2025-05-05"),
  hora_inicio: hora("10:00"),
  hora_fin: hora("16:00"),
  estado: "registrado",
  aval_pdf_url: "http://example.com/aval3.pdf",
  aval_tipo: "director_programa",
  facultad_id: facEcoId
}).insertedId;

const ev4 = db.evento.insertOne({
  nombre_evento: "Festival Deportivo",
  tipo: "ludico",
  descripcion: "Actividades deportivas",
  fecha_evento: new Date("2025-06-01"),
  hora_inicio: hora("08:00"),
  hora_fin: hora("17:00"),
  estado: "registrado",
  aval_pdf_url: "http://example.com/aval4.pdf",
  aval_tipo: "director_docencia",
  facultad_id: facIngId
}).insertedId;

const ev5 = db.evento.insertOne({
  nombre_evento: "Foro Economía Circular",
  tipo: "academico",
  descripcion: "Foro sobre sostenibilidad",
  fecha_evento: new Date("2025-07-20"),
  hora_inicio: hora("09:00"),
  hora_fin: hora("13:00"),
  estado: "en_revision",
  aval_pdf_url: "http://example.com/aval5.pdf",
  aval_tipo: "director_programa",
  facultad_id: facEcoId
}).insertedId;

// =====================================================
//  11. ORGANIZADORES
// =====================================================

registrarOrganizadorEvento(uEst1, ev1);
registrarOrganizadorEvento(uEst2, ev2);
registrarOrganizadorEvento(uDoc1, ev3);
registrarOrganizadorEvento(uDoc2, ev4);
registrarOrganizadorEvento(uEst3, ev5);

// =====================================================
//  12. LUGAR – EVENTO
// =====================================================

db.lugar_evento.insertMany([
  { lugar_id: lug1, evento_id: ev1 },
  { lugar_id: lug3, evento_id: ev2 },
  { lugar_id: lug5, evento_id: ev3 },
  { lugar_id: lug4, evento_id: ev4 },
  { lugar_id: lug2, evento_id: ev5 }
]);

// =====================================================
//  13. ORGANIZACIONES EXTERNAS
// =====================================================

const org1 = db.organizacion_externa.insertOne({
  nombre: "TechEdu SAS",
  nombre_representante_legal: "Carlos Martínez",
  ubicacion: "Cali",
  sector_economico: "Tecnología",
  actividad_principal: "Software educativo",
  numero_contacto: "3001112233"
}).insertedId;

const org2 = db.organizacion_externa.insertOne({
  nombre: "DataLab Consulting",
  nombre_representante_legal: "Lucía Herrera",
  ubicacion: "Bogotá",
  sector_economico: "Consultoría",
  actividad_principal: "Analítica de datos",
  numero_contacto: "3002223344"
}).insertedId;

const org3 = db.organizacion_externa.insertOne({
  nombre: "Emprendimientos Futuro",
  nombre_representante_legal: "Miguel Ruiz",
  ubicacion: "Cali",
  sector_economico: "Servicios",
  actividad_principal: "Aceleradora",
  numero_contacto: "3003334455"
}).insertedId;

const org4 = db.organizacion_externa.insertOne({
  nombre: "Deportes UAO",
  nombre_representante_legal: "Paula Mejía",
  ubicacion: "Cali",
  sector_economico: "Deporte",
  actividad_principal: "Eventos deportivos",
  numero_contacto: "3004445566"
}).insertedId;

const org5 = db.organizacion_externa.insertOne({
  nombre: "EcoCircular ONG",
  nombre_representante_legal: "Juanita Torres",
  ubicacion: "Palmira",
  sector_economico: "Social",
  actividad_principal: "Sostenibilidad",
  numero_contacto: "3005556677"
}).insertedId;

// =====================================================
//  14. PARTICIPACIÓN
// =====================================================

db.participa.insertMany([
  { organizacion_id: org1, evento_id: ev1, certificado_participacion_url: "http://cert1.pdf", asistira_representante_legal: true, nombre_representante_alternativo: null },
  { organizacion_id: org2, evento_id: ev2, certificado_participacion_url: "http://cert2.pdf", asistira_representante_legal: false, nombre_representante_alternativo: "Andrés Téllez" },
  { organizacion_id: org3, evento_id: ev3, certificado_participacion_url: "http://cert3.pdf", asistira_representante_legal: true, nombre_representante_alternativo: null },
  { organizacion_id: org4, evento_id: ev4, certificado_participacion_url: "http://cert4.pdf", asistira_representante_legal: true, nombre_representante_alternativo: null },
  { organizacion_id: org5, evento_id: ev5, certificado_participacion_url: "http://cert5.pdf", asistira_representante_legal: false, nombre_representante_alternativo: "Carolina Vélez" }
]);

// =====================================================
//  15. EVALUACIONES
// =====================================================

evaluarEvento({
  eventoId: ev1,
  usuarioEvaluadorId: uSec1,
  estado: "aprobado",
  justificacion: "Alineado con los objetivos de formación",
  actaPdfUrl: "http://uao.edu.co/actas/acta1.pdf"
});

evaluarEvento({
  eventoId: ev5,
  usuarioEvaluadorId: uSec3,
  estado: "rechazado",
  justificacion: "No presenta suficiente sustento académico",
  actaPdfUrl: "http://uao.edu.co/actas/acta5.pdf"
});

print(" DATOS DE PRUEBA SIGEU_2 CARGADOS CORRECTAMENTE");
