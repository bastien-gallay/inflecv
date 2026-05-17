// Sample CV — John Doe.
//
// Data-driven layout. Pulls everything from `cv-data.typ`. Replace
// the data file with your own to make this your CV.
//
// Layout notes:
//   - Page 1: header + sidebar + first experiences
//   - Page 2+: full-width detailed experiences (no sidebar)
//
// This file is intentionally minimal. Extend with i18n, short
// variants, or custom sections as needed — see the `inflecv` README.

#import "neat-cv-local.typ": (
  cv-continued, cv-page-one, cv-setup, entry,
)
#import "shared/config.typ": *
#import "shared/sidebar.typ": sidebar-content
#import "cv-data.typ": cv-data

#show: cv-setup.with(
  author: author-config,
  accent-color: accent-color,
  header-color: header-color,
  body-font: body-font,
  body-font-size: body-font-size,
  paper-size: paper-size,
  side-width: side-width,
)

// ===========================================================================
// PAGE 1 — header + sidebar + summary
// ===========================================================================

#cv-page-one(
  profile-picture: image("assets/placeholder-photo.svg"),
  sidebar-content(),
  [
    = Experience

    #for exp in cv-data.experiences [
      #entry(
        title: [#exp.title],
        date: [#exp.period.start - #exp.period.end],
        institution: [#exp.company],
        location: [#exp.location],
      )[
        #for line in exp.summary [
          - #line
        ]
        #if exp.stack.len() > 0 [
          #strong[Stack:] #exp.stack.join(", ")
        ]
      ]
    ]

    = Education

    #for edu in cv-data.education [
      #entry(
        title: [#edu.degree],
        date: [#edu.year],
        institution: [#edu.school],
        location: [#edu.location],
      )[
        #edu.details
      ]
    ]
  ],
)

// ===========================================================================
// PAGE 2+ — detailed experiences (optional, expand as needed)
// ===========================================================================

#if cv-data.at("experiences-detailed", default: ()).len() > 0 {
  pagebreak()
  cv-continued[
    = Detailed Experience

    #for exp in cv-data.experiences-detailed [
      #entry(
        title: [#exp.title],
        date: [#exp.period.start - #exp.period.end],
        institution: [#exp.company],
        location: [#exp.location],
      )[
        #if "description" in exp [
          #exp.description
        ]
        #if "sections" in exp [
          #for sect in exp.sections [
            === #sect.title

            #for item in sect.items [
              - #item
            ]
          ]
        ]
      ]
    ]

    = Certifications

    #for cert in cv-data.certifications [
      - *#cert.name* — #cert.issuer (#cert.year)
    ]
  ]
}
