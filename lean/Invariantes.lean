/-
  Gerado por scripts/build.py — NÃO editar à mão.
  Verifica, por `decide`, invariantes estruturais dos 57 mapeamentos de data/mapeamentos.csv.
  Escopo: consistência dos dados (sem exactMatch, ao menos uma fonte, IDs únicos).
  NÃO verifica se cada correspondência está semanticamente correta.
-/
inductive Relacao | related | close | broad | narrow | exact
  deriving DecidableEq, Repr
inductive Status | verificado | aConfirmar
  deriving DecidableEq, Repr

structure Mapeamento where
  id : String
  relacao : Relacao
  status : Status
  nFontes : Nat
  deriving Repr

def mapeamentos : List Mapeamento := [
  ⟨"m01", .close, .verificado, 2⟩,
  ⟨"m02", .close, .verificado, 2⟩,
  ⟨"m03", .close, .verificado, 2⟩,
  ⟨"m04", .close, .verificado, 1⟩,
  ⟨"m05", .related, .verificado, 1⟩,
  ⟨"m06", .related, .verificado, 1⟩,
  ⟨"m07", .related, .verificado, 1⟩,
  ⟨"m08", .related, .verificado, 2⟩,
  ⟨"m09", .related, .verificado, 2⟩,
  ⟨"m10", .related, .verificado, 2⟩,
  ⟨"m11", .related, .verificado, 2⟩,
  ⟨"m12", .related, .verificado, 2⟩,
  ⟨"m13", .related, .verificado, 2⟩,
  ⟨"m14", .related, .verificado, 2⟩,
  ⟨"m15", .related, .verificado, 2⟩,
  ⟨"m16", .related, .verificado, 2⟩,
  ⟨"m17", .related, .verificado, 2⟩,
  ⟨"m18", .related, .verificado, 2⟩,
  ⟨"m19", .related, .verificado, 1⟩,
  ⟨"m20", .related, .verificado, 1⟩,
  ⟨"m21", .related, .aConfirmar, 2⟩,
  ⟨"m22", .related, .verificado, 2⟩,
  ⟨"m23", .related, .verificado, 2⟩,
  ⟨"m24", .related, .verificado, 1⟩,
  ⟨"m25", .related, .verificado, 2⟩,
  ⟨"m26", .related, .verificado, 2⟩,
  ⟨"m27", .related, .verificado, 1⟩,
  ⟨"m28", .related, .verificado, 1⟩,
  ⟨"m29", .related, .verificado, 2⟩,
  ⟨"m30", .related, .verificado, 2⟩,
  ⟨"m31", .related, .verificado, 2⟩,
  ⟨"m32", .related, .aConfirmar, 2⟩,
  ⟨"m33", .related, .aConfirmar, 1⟩,
  ⟨"m34", .related, .verificado, 1⟩,
  ⟨"m35", .related, .verificado, 1⟩,
  ⟨"m36", .related, .aConfirmar, 1⟩,
  ⟨"m37", .related, .verificado, 2⟩,
  ⟨"m38", .related, .aConfirmar, 2⟩,
  ⟨"m39", .related, .verificado, 2⟩,
  ⟨"m40", .related, .verificado, 1⟩,
  ⟨"m41", .related, .verificado, 2⟩,
  ⟨"m42", .related, .verificado, 1⟩,
  ⟨"m43", .related, .verificado, 2⟩,
  ⟨"m44", .related, .verificado, 2⟩,
  ⟨"m45", .related, .verificado, 2⟩,
  ⟨"m46", .related, .verificado, 2⟩,
  ⟨"m47", .related, .aConfirmar, 2⟩,
  ⟨"m48", .related, .aConfirmar, 2⟩,
  ⟨"m49", .close, .verificado, 1⟩,
  ⟨"m50", .related, .verificado, 2⟩,
  ⟨"m51", .related, .aConfirmar, 2⟩,
  ⟨"m52", .close, .verificado, 2⟩,
  ⟨"m53", .related, .aConfirmar, 2⟩,
  ⟨"m54", .related, .verificado, 1⟩,
  ⟨"m55", .related, .aConfirmar, 2⟩,
  ⟨"m56", .related, .aConfirmar, 1⟩,
  ⟨"m57", .related, .verificado, 2⟩
]

theorem sem_exactMatch : mapeamentos.all (fun m => m.relacao != .exact) = true := by decide
theorem toda_correspondencia_tem_fonte : mapeamentos.all (fun m => m.nFontes ≥ 1) = true := by decide
theorem ids_unicos : (mapeamentos.map (·.id)).eraseDups.length = mapeamentos.length := by decide
theorem total : mapeamentos.length = 57 := by decide
