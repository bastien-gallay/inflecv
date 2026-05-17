// cv-data.typ - Données structurées du CV (John Doe — sample)
//
// This is the SAMPLE data shipped with the inflecv toolkit. Replace
// every field below with your own to produce your CV.
//
// Schema stability: the structure (keys, types, nesting) is part of
// the public contract. The values are illustrative.
//
// Usage:
//   #import "cv-data.typ": cv-data
//   #cv-data.personal.firstname

#let cv-data = (
  // ============================================================
  // PERSONAL
  // ============================================================
  personal: (
    firstname: "John",
    lastname: "Doe",
    email: "john.doe@example.com",
    phone: "(+1) 555-0123",
    address: "Anytown, World",
    position: "Senior Backend Engineer | Distributed Systems",
    photo: "assets/placeholder-photo.svg",
    nationality: "Worldwide",
    birthdate: "01/01/1990",
  ),

  // ============================================================
  // SOCIAL
  // ============================================================
  social: (
    linkedin: "johndoe",
    github: "johndoe",
    website: "johndoe.example.com",
  ),

  // ============================================================
  // ABOUT
  // ============================================================
  about: "Senior backend engineer with 8 years of production experience in distributed systems, Python, and PostgreSQL. Builds reliable ingestion pipelines and partner-facing APIs.",

  // ============================================================
  // INTERESTS
  // ============================================================
  interests: (
    "Distributed systems",
    "Open-source contribution",
    "Mentoring",
  ),

  // ============================================================
  // INFLUENCE / OUTREACH
  // ============================================================
  influence: (
    "FastAPI contributor (3 merged PRs)",
    "Local Python meetup organiser",
  ),

  // ============================================================
  // LANGUAGES
  // ============================================================
  languages: (
    (name: "English", level: 5, subtitle: "Native"),
    (name: "French", level: 3, subtitle: "Conversational"),
  ),

  // ============================================================
  // SKILLS
  // ============================================================
  skills: (
    methodologies: (
      "Scrum",
      "Kanban",
      "Trunk-based development",
    ),
    practices: (
      "Test-Driven Development",
      "Domain-Driven Design",
      "Pair programming",
      "Postmortem culture",
    ),
    technologies: (
      "Python",
      "Go",
      "PostgreSQL",
      "Kafka",
      "Redis",
      "FastAPI",
      "Docker",
      "Kubernetes",
    ),
    roles: (
      "Backend engineering",
      "Architecture",
      "Mentoring",
    ),
    all: (
      "Python",
      "Go",
      "PostgreSQL",
      "Kafka",
      "Redis",
      "FastAPI",
      "Docker",
      "Kubernetes",
      "Test-Driven Development",
      "Domain-Driven Design",
      "Scrum",
      "Mentoring",
    ),
  ),

  // ============================================================
  // EXPERIENCES (summary)
  // ============================================================
  experiences: (
    (
      id: "acme-platform",
      title: "Senior Backend Engineer",
      company: "Example Platform Co.",
      location: "Remote (EU)",
      period: (start: "01/2022", end: "Present"),
      summary: (
        "Owned ingestion pipelines (~50 GB/day) and partner API consumed by 30+ integrators.",
        "Led idempotency rewrite reducing duplicate-event incidents by 90%.",
        "Mentored 3 mid-level engineers; one promoted to senior.",
      ),
      stack: ("Python", "Go", "Kafka", "PostgreSQL", "Kubernetes"),
    ),
    (
      id: "fintech-startup",
      title: "Backend Engineer",
      company: "Sample Fintech Startup",
      location: "Remote",
      period: (start: "06/2019", end: "12/2021"),
      summary: (
        "Built core ledger service handling 1M+ daily transactions.",
        "Designed online migration strategy for 200M-row table using pg_repack + dual-write.",
      ),
      stack: ("Python", "FastAPI", "PostgreSQL", "Redis"),
    ),
    (
      id: "first-job",
      title: "Software Engineer",
      company: "Generic SaaS Vendor",
      location: "Berlin, DE",
      period: (start: "08/2016", end: "05/2019"),
      summary: (
        "Maintained REST API consumed by 200+ enterprise customers.",
        "Introduced pre-commit hooks reducing CI failures by 40%.",
      ),
      stack: ("Python", "Flask", "PostgreSQL", "Docker"),
    ),
  ),

  // ============================================================
  // EXPERIENCES (detailed — adapt as needed)
  // ============================================================
  experiences-detailed: (
    (
      id: "acme-platform",
      title: "Senior Backend Engineer",
      company: "Example Platform Co.",
      location: "Remote (EU)",
      period: (start: "01/2022", end: "Present"),
      description: "Senior individual contributor on an 8-person platform team scaling 10x year over year.",
      sections: (
        (
          title: "Ingestion & Reliability",
          items: (
            "Owned ~50 GB/day ingestion pipelines with end-to-end observability.",
            "Idempotency rewrite: 90% reduction in duplicate-event incidents.",
            "Implemented backpressure and dead-letter queues using Kafka.",
          ),
        ),
        (
          title: "Partner API",
          items: (
            "Designed v2 partner API consumed by 30+ external integrators.",
            "Versioning policy with 12-month deprecation windows.",
            "On-call rotation: 1 week / 6, with postmortem authoring.",
          ),
        ),
        (
          title: "Mentoring",
          items: (
            "Mentored 3 mid-level engineers; one promoted to senior.",
            "Authored internal Tidy First playbook.",
          ),
        ),
      ),
      stack: (
        languages: ("Python", "Go"),
        infra: ("Kubernetes", "Kafka", "PostgreSQL", "Redis"),
        methods: ("Trunk-based development", "TDD", "Postmortems"),
      ),
    ),
  ),

  // ============================================================
  // EDUCATION (summary)
  // ============================================================
  education: (
    (
      id: "ms-cs",
      degree: "M.Sc. Computer Science",
      school: "Example University",
      location: "Sample City, World",
      year: "2016",
      details: "Thesis: Distributed consensus under partial failures.",
    ),
  ),

  // ============================================================
  // EDUCATION (detailed)
  // ============================================================
  education-detailed: (
    (
      id: "ms-cs",
      degree: "M.Sc. Computer Science",
      school: "Example University",
      location: "Sample City, World",
      year: "2016",
      details: "Thesis: Distributed consensus under partial failures.",
    ),
    (
      id: "bs-cs",
      degree: "B.Sc. Computer Science",
      school: "Example University",
      location: "Sample City, World",
      year: "2014",
      details: "Honours project: Lock-free queue implementations benchmark.",
    ),
  ),

  // ============================================================
  // CERTIFICATIONS
  // ============================================================
  certifications: (
    (name: "Certified Kubernetes Administrator (CKA)", issuer: "CNCF", year: "2023"),
    (name: "Professional Scrum Master I (PSM-I)", issuer: "Scrum.org", year: "2020"),
  ),

  // ============================================================
  // VOLUNTEERING
  // ============================================================
  volunteering: (
    (
      title: "Python Meetup Organiser",
      organization: "Sample Python Community",
      location: "Sample City",
      period: "2019 - Present",
      items: (
        "Organise quarterly meetups (40-60 attendees).",
        "Coordinate speakers and venues.",
      ),
    ),
  ),

  // ============================================================
  // STYLE (informational)
  // ============================================================
  style: (
    accent-color: "#4682b4",
    header-color: "#3b4f60",
    body-font-size: "10pt",
    paper-size: "a4",
    side-width: "4.5cm",
  ),
)
