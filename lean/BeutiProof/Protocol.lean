import Lean

namespace BeutiProof

/-- Smoke-test output. This value is not an analysis report. -/
def scaffoldStatus : Lean.Json :=
  Lean.Json.mkObj [
    ("schema_version", Lean.toJson ("0.1.0" : String)),
    ("status", Lean.toJson ("scaffold" : String)),
    ("analysis_available", Lean.toJson false)
  ]

end BeutiProof
