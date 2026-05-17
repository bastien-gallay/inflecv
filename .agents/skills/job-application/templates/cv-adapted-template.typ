// Template de CV adapté
// Copier ce fichier vers data/applications/{app_id}/{app_id}-cv-adapted.typ
// et personnaliser selon l'analyse

// Imports depuis data/applications/{app_id}/ (3 niveaux de profondeur)
#import "../../../src/neat-cv-local.typ": (
  cv-continued, cv-page-one, cv-setup, email-link, entry, publications,
  contact-info, item-pills, social-links,
)

// Configuration de base
#import "../../../src/shared/config.typ": *

// Expériences modulaires
#import "../../../src/shared/experiences.typ": *

// Sections additionnelles
#import "../../../src/shared/sections.typ": *

// =============================================================================
// MÉTADONNÉES DOCUMENT
// =============================================================================

// TODO: Adapter le titre avec le poste et l'entreprise
#set document(
  title: "CV - {Firstname} {Lastname} - {Position} @ {Company}",
  author: "{Firstname} {Lastname}",
  date: datetime.today(),
)

// =============================================================================
// CONFIGURATION ADAPTÉE
// =============================================================================

// Modifier le titre du poste si pertinent pour l'offre
#let author-adapted = (
  ..author-config,
  // Exemple: position: "CTO | Expert Cloud & IA"
  position: author-config.position,
)

// =============================================================================
// SIDEBAR ADAPTÉE
// =============================================================================

// Texte "A propos" adapté à l'offre
// Reformuler pour mettre en avant les aspects pertinents
#let about-text-adapted = [
  // TODO: Adapt to the target offer.
  // Sample (John Doe): Senior backend engineer, 8 years building reliable
  // distributed systems. Strong PostgreSQL and event-driven systems.
]

// Skills réordonnés selon l'offre
// Mettre en premier les compétences demandées
#let skills-leadership-adapted = (
  // TODO: Réordonner selon l'offre
  "COMEX",
  "Recrutement",
  "Stratégie Tech",
  "Formation",
)

#let skills-tech-adapted = (
  // TODO: Réordonner selon l'offre, ajouter si possédés
  "GenAI Dev",
  "Python",
  "TypeScript",
  "Azure",
  "React",
  "Node.js",
  "C#",
  "Rust",
)

#let skills-methodo-adapted = (
  // TODO: Réordonner selon l'offre
  "SAFe",
  "Lean Startup",
  "Craftsmanship",
  "TDD",
  "DDD",
)

#let sidebar-adapted() = [
  = A propos
  #about-text-adapted

  = Rayonnement
  - Mentor Google Launchpad
  - Coach Startup Weekend
  - Orateur Agile Tour & Scrum Day

  = Contact
  #contact-info()

  = Informations
  Nationalité : Français

  Date de naissance : 3/03/1979

  #social-links()

  - *Français :* Langue maternelle
  - *Anglais :* Courant

  = Leadership
  #item-pills(skills-leadership-adapted)

  = Tech & IA
  #item-pills(skills-tech-adapted)

  = Méthodologie
  #item-pills(skills-methodo-adapted)
]

// =============================================================================
// EXPÉRIENCES ADAPTÉES
// =============================================================================

// Réordonner les expériences selon leur pertinence pour le poste
// Commenter/décommenter selon le niveau de détail souhaité
#let experiences-adapted = [
  = Expérience Professionnelle

  // TODO: Réordonner selon la pertinence
  // Les plus pertinentes en premier
  #exp-palo-it
  #exp-upwiser
  #exp-cdiscount
  #exp-cast
  // #exp-dev-web  // Omettre si non pertinent
]

// =============================================================================
// SECTIONS ADDITIONNELLES
// =============================================================================

#let sections-adapted = [
  #section-formation
  #section-certifications
  #section-engagement
]

// =============================================================================
// DOCUMENT
// =============================================================================

#show: cv-setup.with(
  author: author-adapted,
  accent-color: accent-color,
  header-color: header-color,
  body-font: body-font,
  body-font-size: body-font-size,
  paper-size: paper-size,
  side-width: side-width,
)

#cv-page-one(
  profile-picture: image("../../../src/assets/photo-profile-pro.jpg"),
  sidebar-adapted(),
  [
    #experiences-adapted
    #sections-adapted
  ],
)

// =============================================================================
// PAGES ADDITIONNELLES (si version longue)
// =============================================================================

// Décommenter pour version longue avec détails
// #pagebreak()
// #cv-continued[
//   = Expérience détaillée
//   // Ajouter les détails des expériences pertinentes
// ]
