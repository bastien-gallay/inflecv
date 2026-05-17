// Sidebar content — data-driven from cv-data.typ.
//
// This is intentionally minimal. Extend with i18n, custom sections,
// or per-CV-variant logic as needed.

#import "../neat-cv-local.typ": contact-info, item-pills, social-links
#import "../cv-data.typ": cv-data

#let sidebar-content() = [
  = About

  #cv-data.about

  = Contact

  #contact-info()

  #social-links()

  = Languages

  #for lang in cv-data.languages [
    - *#lang.name:* #lang.subtitle
  ]

  = Skills

  #item-pills(cv-data.skills.all)

  #if "influence" in cv-data and cv-data.influence.len() > 0 [
    = Outreach

    #for line in cv-data.influence [
      - #line
    ]
  ]
]
