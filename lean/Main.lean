import BeutiProof

/-- Emit the build smoke-test status, not a proof-quality assessment. -/
def main : IO Unit :=
  IO.println BeutiProof.scaffoldStatus.compress
