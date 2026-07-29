---
headword: break-glass
pos: n. attrib. & n.
class: vogue
senses:
  - label: information security
    definition: >
      Designating an identity, credential, or access path deliberately
      exempted from a system's otherwise-universal denials and held dormant
      for emergencies — recovery, revocation, repair — every invocation
      logged; distinguished from a standing administrator account by
      exemption and dormancy rather than by privilege.
    example: >
      The bucket policy denies deletes to everyone except the break-glass
      role, and any use of that role lands in the audit trail.
  - label: organizational computing
    definition: >
      The exemption mechanism itself, whether a policy carve-out or a
      procedure-gated ceremony; a system's named emergency door, as distinct
      from an undocumented hole.
first_use:
  date: "2005"
  type: published
  url: https://hipaa.yale.edu/security/break-glass-procedure-granting-emergency-access-critical-ephi-systems
  source: >
    Yale HIPAA Security, "Break Glass Procedure"
  note: >
    Approximate. From fire-alarm signage ("break glass in case of
    emergency"); in healthcare-IT usage as "break-the-glass" emergency
    access to patient records by the mid-2000s, under the 2003 HIPAA
    Security Rule's emergency-access provision (the rule mandates the
    procedure, not the name); later standard in cloud privileged-access
    design. The machine-speech expansion is range: from emergency *account*
    to any deny-exempt principal, path, or ceremony in policy design
attestation:
  model: Claude Fable 5
  date: 2026-07-29
  observer: chrismerck
---
