// Shared configuration for all CV versions.
// Used by cv.typ, cv-short.typ, cv-en.typ, cv-en-short.typ.
//
// Sample data — replace with your own. See cv-data.typ for the
// recommended single-source-of-truth pattern.

// Author info
#let author-config = (
  firstname: "John",
  lastname: "Doe",
  email: "john.doe@example.com",
  address: [Anytown, World],
  phone: "(+1) 555-0123",
  position: "Senior Backend Engineer | Distributed Systems",
  linkedin: "johndoe",
)

// Couleurs
#let accent-color = rgb("#4682b4")
#let header-color = rgb("#3b4f60")

// Typographie
#let body-font = "Helvetica Neue"
#let body-font-size = 10pt

// Langue par défaut
#let cv-lang = "fr"

// Mise en page
#let paper-size = "a4"
#let side-width = 4.5cm
