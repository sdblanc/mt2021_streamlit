# Appendix: Horus accepted tax combinations (sales and purchases)

Source: the two spreadsheets linked from the Horus API reference pages of `invoices.sales.new` / `invoices.sales.update` ("The accepted tax combinations (Tax rate / origin and type) are available here") and `invoices.purchases.new` / `invoices.purchases.update` ("The accepted tax combinations (Tax type / kind / rate / origin / condition / condition value)) are available here"):
- https://horus-technical-documents.s3.eu-central-1.amazonaws.com/Tax-combinations-sales.xlsx
- https://horus-technical-documents.s3.eu-central-1.amazonaws.com/Tax-combinations-purchases.xlsx

Downloaded 13 Oct 2026 and converted mechanically to text (cell values only, sheet by sheet, ' | ' between columns). No content was edited; source typos (e.g. 'Nationam') are kept. 'XX' in the sales OSS rows is as in the source (rate and country supplied per transaction).

## Tax-combinations-sales.xlsx

### Sheet: Combinations (BE) (18 rows)

```text
Legislation | TaxType | TaxType | TaxRate | TaxOrigin | TaxCountryCode | TaxOrigin
BE | 0 | National | 0 | 0 |  | Vente nationale / Verkopen
BE | 0 | National | 0 | 1 |  | Vente Cocontractant / Verkopen Medekontraktant
BE | 0 | National | 0 | 2 |  | Exemption Art 44 / Vrijstellingen Art 44
BE | 0 | National | 0 | 4 |  | Vidanges-Emballages / Leeggoed-Verpakking
BE | 0 | National | 0 | 5 |  | Escompte / Diskonto
BE | 0 | National | 0 | 6 |  | Autre exemption / Andere Vrijstellingen
BE | 0 | National | 0 | 7 |  | Autre exemption avec MAJ du C.A. / andere Vrijstell. met UPD v/d Omzet
BE | 0 | National | 6 | 0 |  | Vente nationale / Verkopen
BE | 0 | National | 12 | 0 |  | Vente nationale / Verkopen
BE | 0 | National | 21 | 0 |  | Vente nationale / Verkopen
BE | 0 | National | 21 | 3 |  | Vente Taxe d'égalisation / Verkopen EgalisatieBelasting
BE | 1 | European | 0 | 8 |  | Transfert de biens / Overdracht van Goederen
BE | 1 | European | 0 | 9 |  | Ventes Marchandises / Verkopen Handelsgoederen
BE | 1 | European | 0 | 10 |  | Livraison avec installation / Leveringen met installatie
BE | 1 | European | 0 | 11 |  | Prestation hors Belgique / Diensten Buiten België
BE | 1 | European | 0 | 12 |  | Travail à façon / Maakloonwerk
BE | 1 | European | XX | 13 | XX | (OSS) Vente taxe soumis dans le pays européen / Verkoopbelasting ingediend in het Europese land
BE | 2 | International | 0 | 14 |  | Exportations / Export
```

### Sheet: Combinations (LU) (58 rows)

```text
Legislation | TaxType | TaxType | TaxRate | TaxOrigin | TaxCountryCode | TaxOrigin
LU | 0 | National | 3 | 15 |  | Ventes produits fabriqués
LU | 0 | National | 8 | 15 |  | Ventes produits fabriqués
LU | 0 | National | 7 | 15 |  | Ventes produits fabriqués
LU | 0 | National | 13 | 15 |  | Ventes produits fabriqués
LU | 0 | National | 14 | 15 |  | Ventes produits fabriqués
LU | 0 | National | 17 | 15 |  | Ventes produits fabriqués
LU | 0 | National | 16 | 15 |  | Ventes produits fabriqués
LU | 0 | National | 3 | 9 |  | Ventes marchandises
LU | 0 | National | 8 | 9 |  | Ventes marchandises
LU | 0 | National | 7 | 9 |  | Ventes marchandises
LU | 0 | National | 13 | 9 |  | Ventes marchandises
LU | 0 | National | 14 | 9 |  | Ventes marchandises
LU | 0 | National | 17 | 9 |  | Ventes marchandises
LU | 0 | National | 16 | 9 |  | Ventes marchandises
LU | 0 | National | 3 | 18 |  | Ventes prestations de services
LU | 0 | National | 8 | 18 |  | Ventes prestations de services
LU | 0 | National | 7 | 18 |  | Ventes prestations de services
LU | 0 | National | 13 | 18 |  | Ventes prestations de services
LU | 0 | National | 14 | 18 |  | Ventes prestations de services
LU | 0 | National | 17 | 18 |  | Ventes prestations de services
LU | 0 | National | 16 | 18 |  | Ventes prestations de services
LU | 0 | National | 3 | 16 |  | Ventes d'immobilisés
LU | 0 | National | 8 | 16 |  | Ventes d'immobilisés
LU | 0 | National | 7 | 16 |  | Ventes d'immobilisés
LU | 0 | National | 14 | 16 |  | Ventes d'immobilisés
LU | 0 | National | 13 | 16 |  | Ventes d'immobilisés
LU | 0 | National | 16 | 16 |  | Ventes d'immobilisés
LU | 0 | National | 17 | 16 |  | Ventes d'immobilisés
LU | 0 | National | 3 | 19 |  | Ventes autres
LU | 0 | National | 8 | 19 |  | Ventes autres
LU | 0 | National | 7 | 19 |  | Ventes autres
LU | 0 | National | 13 | 19 |  | Ventes autres
LU | 0 | National | 14 | 19 |  | Ventes autres
LU | 0 | National | 17 | 19 |  | Ventes autres
LU | 0 | National | 16 | 19 |  | Ventes autres
LU | 0 | National | 0 | 17 |  | Ventes de tabacs
LU | 0 | National | 0 | 35 |  | Utilisation privée de biens
LU | 0 | National | 3 | 35 |  | Utilisation privée de biens
LU | 0 | National | 8 | 35 |  | Utilisation privée de biens
LU | 0 | National | 7 | 35 |  | Utilisation privée de biens
LU | 0 | National | 13 | 35 |  | Utilisation privée de biens
LU | 0 | National | 14 | 35 |  | Utilisation privée de biens
LU | 0 | National | 17 | 35 |  | Utilisation privée de biens
LU | 0 | National | 16 | 35 |  | Utilisation privée de biens
LU | 1 | European | 0 | 27 |  | UE - Ventes Marchandises - triangulaire
LU | 1 | European | XX | 26 | XX | (OSS) UE - Ventes Marchandises - distance
LU | 1 | European | 0 | 28 |  | UE - Ventes produits fabriqués
LU | 1 | European | XX | 29 | XX | (OSS) UE - Ventes produits fabriqués - distance
LU | 1 | European | 0 | 20 |  | UE - Prestation de services - exo pays acheteur
LU | 1 | European | 0 | 21 |  | UE - Prestation de services - taxable pays acheteur
LU | 1 | European | 0 | 22 |  | UE - Vente d'immobilisés
LU | 1 | European | 0 | 23 |  | UE - Ventes autres
LU | 1 | European | XX | 24 | XX | (OSS) UE - Ventes autres - taxe étrangère
LU | 2 | International | 0 | 33 |  | Export - Produits fabriqués
LU | 2 | International | 0 | 31 |  | Export - Marchandises
LU | 2 | International | 0 | 32 |  | Export - Prestations de services
LU | 2 | International | 0 | 34 |  | Export - Ventes immobilisés
LU | 2 | International | 0 | 30 |  | Export - Autres
```

### Sheet: Available values (37 rows)

```text
 | TaxOrigin
 | 0 | Vente nationale
 | 1 | Vente Cocontractant
 | 2 | Exemption Art 44
 | 3 | Vente Taxe d'égalisation
 | 4 | Vidanges-Emballages
 | 5 | Escompte
 | 6 | Autre exemption
 | 7 | Autre exemption avec MAJ du C.A.
 | 8 | Transfert de biens
 | 9 | Ventes Marchandises
 | 10 | Livraison avec installation
 | 11 | Prestation hors Belgique
 | 12 | Travail à façon
 | 13 | Vente taxe soumis dans le pays européen
 | 14 | Exportations
 | 15 | Ventes produits fabriqués
 | 16 | Ventes d'immobilisés
 | 17 | Ventes de tabacs
 | 18 | Ventes prestations de services
 | 19 | Ventes autres
 | 20 | UE - Prestation de services - exo pays acheteur
 | 21 | UE - Prestation de services - taxable pays acheteur
 | 22 | UE - Vente d'immobilisés
 | 23 | UE - Ventes autres
 | 24 | UE - Ventes autres - taxe étrangère
 | 25 | UE - Ventes Marchandises
 | 26 | UE - Ventes Marchandises - distance
 | 27 | UE - Ventes Marchandises - triangulaire
 | 28 | UE - Ventes produits fabriqués
 | 29 | UE - Ventes produits fabriqués - distance
 | 30 | Export - Autres
 | 31 | Export - Marchandises
 | 32 | Export - Prestations de services
 | 33 | Export - Produits fabriqués
 | 34 | Export - Ventes immobilisés
 | 35 | Utilisation privée de biens
```

## Tax-combinations-purchases.xlsx

### Sheet: Combinations (BE) (109 rows)

```text
Legislation | TaxType | TaxType | TaxKind | TaxKind | TaxRate | TaxCondition | TaxCondition | TaxConditionValue | TaxConditionValue | TaxOrigin | TaxOrigin - FR | TaxOrigin - NL | OrderView (to ignore)
BE | 0 | National | 0 | MERCH | 0 |  |  |  |  | 2 | Achat Marchandises | Achat Marchandises | 20
BE | 0 | National | 0 | MERCH | 6 | 1 | DEDUC | true | TRUE | 2 | Achat Marchandises | Achat Marchandises | 21
BE | 0 | National | 0 | MERCH | 6 | 1 | DEDUC | false | FALSE | 2 | Achat Marchandises | Achat Marchandises | 21
BE | 0 | National | 0 | MERCH | 12 | 1 | DEDUC | true | TRUE | 2 | Achat Marchandises | Achat Marchandises | 22
BE | 0 | National | 0 | MERCH | 12 | 1 | DEDUC | false | FALSE | 2 | Achat Marchandises | Achat Marchandises | 22
BE | 0 | National | 0 | MERCH | 21 | 1 | DEDUC | true | TRUE | 2 | Achat Marchandises | Achat Marchandises | 23
BE | 0 | National | 0 | MERCH | 21 | 1 | DEDUC | false | FALSE | 2 | Achat Marchandises | Achat Marchandises | 23
BE | 0 | National | 1 | GS | 0 |  |  |  |  | 0 | Achat Biens et Services | Achat Biens et Services | 24
BE | 0 | National | 1 | GS | 6 | 1 | DEDUC | true | TRUE | 0 | Achat Biens et Services | Achat Biens et Services | 25
BE | 0 | National | 1 | GS | 6 | 1 | DEDUC | false | FALSE | 0 | Achat Biens et Services | Achat Biens et Services | 25
BE | 0 | National | 1 | GS | 12 | 1 | DEDUC | true | TRUE | 0 | Achat Biens et Services | Achat Biens et Services | 26
BE | 0 | National | 1 | GS | 12 | 1 | DEDUC | false | FALSE | 0 | Achat Biens et Services | Achat Biens et Services | 26
BE | 0 | National | 1 | GS | 21 | 1 | DEDUC | true | TRUE | 0 | Achat Biens et Services | Achat Biens et Services | 27
BE | 0 | National | 1 | GS | 21 | 1 | DEDUC | false | FALSE | 0 | Achat Biens et Services | Achat Biens et Services | 27
BE | 0 | National | 2 | INVES | 0 |  |  |  |  | 1 | Achat Investissements | Achat Investissements | 28
BE | 0 | National | 2 | INVES | 6 | 1 | DEDUC | true | TRUE | 1 | Achat Investissements | Achat Investissements | 29
BE | 0 | National | 2 | INVES | 6 | 1 | DEDUC | false | FALSE | 1 | Achat Investissements | Achat Investissements | 29
BE | 0 | National | 2 | INVES | 12 | 1 | DEDUC | true | TRUE | 1 | Achat Investissements | Achat Investissements | 30
BE | 0 | National | 2 | INVES | 12 | 1 | DEDUC | false | FALSE | 1 | Achat Investissements | Achat Investissements | 30
BE | 0 | National | 2 | INVES | 21 | 1 | DEDUC | true | TRUE | 1 | Achat Investissements | Achat Investissements | 31
BE | 0 | National | 2 | INVES | 21 | 1 | DEDUC | false | FALSE | 1 | Achat Investissements | Achat Investissements | 31
BE | 0 | Nationam | 0 | MERCH | 0 |  |  |  |  | 12 | Achat TVA Marge | Achat TVA Marge | 32
BE | 0 | National | 1 | GS | 21 | 3 | PCT | 35 | 35 % | 10 | Frais de voiture / Multimédia | Frais de voiture / Multimédia | 33
BE | 0 | National | 1 | GS | 21 | 3 | PCT | 50 | 50 % | 10 | Frais de voiture / Multimédia | Frais de voiture / Multimédia | 33
BE | 0 | National | 1 | GS | 21 | 3 | PCT | 75 | 75 % | 10 | Frais de voiture / Multimédia | Frais de voiture / Multimédia | 33
BE | 0 | National | 1 | GS | 21 | 3 | PCT | 85 | 85 % | 10 | Frais de voiture / Multimédia | Frais de voiture / Multimédia | 33
BE | 0 | National | 2 | INVES | 21 | 3 | PCT | 35 | 35 % | 18 | Investissement partiellement récupérable | Investissement partiellement récupérable | 34
BE | 0 | National | 2 | INVES | 21 | 3 | PCT | 50 | 50 % | 18 | Investissement partiellement récupérable | Investissement partiellement récupérable | 34
BE | 0 | National | 2 | INVES | 21 | 3 | PCT | 75 | 75 % | 18 | Investissement partiellement récupérable | Investissement partiellement récupérable | 34
BE | 0 | National | 2 | INVES | 21 | 3 | PCT | 85 | 85 % | 18 | Investissement partiellement récupérable | Investissement partiellement récupérable | 34
BE | 0 | National | 1 | GS | 0 |  |  |  |  | 8 | Cocontractant immobilier | Cocontractant immobilier | 35
BE | 0 | National | 1 | GS | 6 | 1 | DEDUC | true | TRUE | 8 | Cocontractant immobilier | Cocontractant immobilier | 36
BE | 0 | National | 1 | GS | 6 | 1 | DEDUC | false | FALSE | 8 | Cocontractant immobilier | Cocontractant immobilier | 36
BE | 0 | National | 1 | GS | 21 | 1 | DEDUC | true | TRUE | 8 | Cocontractant immobilier | Cocontractant immobilier | 37
BE | 0 | National | 1 | GS | 21 | 1 | DEDUC | false | FALSE | 8 | Cocontractant immobilier | Cocontractant immobilier | 37
BE | 0 | National | 2 | INVES | 0 |  |  |  |  | 8 | Cocontractant immobilier | Cocontractant immobilier | 38
BE | 0 | National | 2 | INVES | 6 | 1 | DEDUC | true | TRUE | 8 | Cocontractant immobilier | Cocontractant immobilier | 39
BE | 0 | National | 2 | INVES | 6 | 1 | DEDUC | false | FALSE | 8 | Cocontractant immobilier | Cocontractant immobilier | 39
BE | 0 | National | 2 | INVES | 21 | 1 | DEDUC | true | TRUE | 8 | Cocontractant immobilier | Cocontractant immobilier | 40
BE | 0 | National | 2 | INVES | 21 | 1 | DEDUC | false | FALSE | 8 | Cocontractant immobilier | Cocontractant immobilier | 40
BE | 0 | National |  |  | 0 |  |  |  |  | 39 | Vidanges-Emballages | Vidanges-Emballages | 41
BE | 0 | National |  |  | 0 |  |  |  |  | 9 | Escompte | Escompte | 42
BE | 0 | National |  |  | 0 |  |  |  |  | 4 | Autres exemptions | Autres exemptions | 43
BE | 0 | National |  |  | 0 |  |  |  |  | 5 | Autres exemptions avec MAJ du C.A. | Autres exemptions avec MAJ du C.A. | 44
BE | 0 | National | 0 | MERCH | 21 | 2 | INVEST | false | FALSE | 28 | Prestations de sous-traitance | Prestations de sous-traitance | 45
BE | 0 | National | 0 | MERCH | 21 | 2 | INVEST | true | TRUE | 28 | Prestations de sous-traitance | Prestations de sous-traitance | 45
BE | 1 | European | 0 | MERCH | 0 |  |  |  |  | 25 | Marchandises Intracommunautaires | Marchandises Intracommunautaires | 46
BE | 1 | European | 0 | MERCH | 6 | 1 | DEDUC | true | TRUE | 25 | Marchandises Intracommunautaires | Marchandises Intracommunautaires | 47
BE | 1 | European | 0 | MERCH | 6 | 1 | DEDUC | false | FALSE | 25 | Marchandises Intracommunautaires | Marchandises Intracommunautaires | 47
BE | 1 | European | 0 | MERCH | 12 | 1 | DEDUC | true | TRUE | 25 | Marchandises Intracommunautaires | Marchandises Intracommunautaires | 48
BE | 1 | European | 0 | MERCH | 12 | 1 | DEDUC | false | FALSE | 25 | Marchandises Intracommunautaires | Marchandises Intracommunautaires | 48
BE | 1 | European | 0 | MERCH | 21 | 1 | DEDUC | true | TRUE | 25 | Marchandises Intracommunautaires | Marchandises Intracommunautaires | 49
BE | 1 | European | 0 | MERCH | 21 | 1 | DEDUC | false | FALSE | 25 | Marchandises Intracommunautaires | Marchandises Intracommunautaires | 49
BE | 1 | European | 1 | GS | 0 |  |  |  |  | 6 | Biens Intracommunautaires | Biens Intracommunautaires | 50
BE | 1 | European | 1 | GS | 6 | 1 | DEDUC | true | TRUE | 6 | Biens Intracommunautaires | Biens Intracommunautaires | 51
BE | 1 | European | 1 | GS | 6 | 1 | DEDUC | false | FALSE | 6 | Biens Intracommunautaires | Biens Intracommunautaires | 51
BE | 1 | European | 1 | GS | 12 | 1 | DEDUC | true | TRUE | 6 | Biens Intracommunautaires | Biens Intracommunautaires | 52
BE | 1 | European | 1 | GS | 12 | 1 | DEDUC | false | FALSE | 6 | Biens Intracommunautaires | Biens Intracommunautaires | 52
BE | 1 | European | 1 | GS | 21 | 1 | DEDUC | true | TRUE | 6 | Biens Intracommunautaires | Biens Intracommunautaires | 53
BE | 1 | European | 1 | GS | 21 | 1 | DEDUC | false | FALSE | 6 | Biens Intracommunautaires | Biens Intracommunautaires | 53
BE | 1 | European | 1 | GS | 21 | 3 | PCT | 35 | 35 % | 16 | Biens Intracom. part. déduc. | Biens Intracom. part. déduc. | 54
BE | 1 | European | 1 | GS | 21 | 3 | PCT | 50 | 50 % | 16 | Biens Intracom. part. déduc. | Biens Intracom. part. déduc. | 54
BE | 1 | European | 1 | GS | 21 | 3 | PCT | 75 | 75 % | 16 | Biens Intracom. part. déduc. | Biens Intracom. part. déduc. | 54
BE | 1 | European | 1 | GS | 21 | 3 | PCT | 85 | 85 % | 16 | Biens Intracom. part. déduc. | Biens Intracom. part. déduc. | 54
BE | 1 | European | 1 | GS | 0 |  |  |  |  | 35 | Services Intracommunautaires | Services Intracommunautaires | 55
BE | 1 | European | 1 | GS | 6 | 1 | DEDUC | true | TRUE | 35 | Services Intracommunautaires | Services Intracommunautaires | 56
BE | 1 | European | 1 | GS | 6 | 1 | DEDUC | false | FALSE | 35 | Services Intracommunautaires | Services Intracommunautaires | 56
BE | 1 | European | 1 | GS | 12 | 1 | DEDUC | true | TRUE | 35 | Services Intracommunautaires | Services Intracommunautaires | 57
BE | 1 | European | 1 | GS | 12 | 1 | DEDUC | false | FALSE | 35 | Services Intracommunautaires | Services Intracommunautaires | 57
BE | 1 | European | 1 | GS | 21 | 1 | DEDUC | true | TRUE | 35 | Services Intracommunautaires | Services Intracommunautaires | 58
BE | 1 | European | 1 | GS | 21 | 1 | DEDUC | false | FALSE | 35 | Services Intracommunautaires | Services Intracommunautaires | 58
BE | 1 | European | 1 | GS | 21 | 3 | PCT | 35 | 35 % | 22 | Services Intracom. part. déduc. | Services Intracom. part. déduc. | 59
BE | 1 | European | 1 | GS | 21 | 3 | PCT | 50 | 50 % | 22 | Services Intracom. part. déduc. | Services Intracom. part. déduc. | 59
BE | 1 | European | 1 | GS | 21 | 3 | PCT | 75 | 75 % | 22 | Services Intracom. part. déduc. | Services Intracom. part. déduc. | 59
BE | 1 | European | 1 | GS | 21 | 3 | PCT | 85 | 85 % | 22 | Services Intracom. part. déduc. | Services Intracom. part. déduc. | 59
BE | 1 | European | 2 | INVES | 0 |  |  |  |  | 17 | Investissement biens Intracom. | Investissement biens Intracom. | 60
BE | 1 | European | 2 | INVES | 21 | 1 | DEDUC | true | TRUE | 17 | Investissement biens Intracom. | Investissement biens Intracom. | 61
BE | 1 | European | 2 | INVES | 21 | 1 | DEDUC | false | FALSE | 17 | Investissement biens Intracom. | Investissement biens Intracom. | 61
BE | 1 | European | 2 | INVES | 21 | 3 | PCT | 35 | 35 % | 23 | Investissement biens Intracom. part. déduc. | Investissement biens Intracom. part. déduc. | 62
BE | 1 | European | 2 | INVES | 21 | 3 | PCT | 50 | 50 % | 23 | Investissement biens Intracom. part. déduc. | Investissement biens Intracom. part. déduc. | 62
BE | 1 | European | 2 | INVES | 21 | 3 | PCT | 75 | 75 % | 23 | Investissement biens Intracom. part. déduc. | Investissement biens Intracom. part. déduc. | 62
BE | 1 | European | 2 | INVES | 21 | 3 | PCT | 85 | 85 % | 23 | Investissement biens Intracom. part. déduc. | Investissement biens Intracom. part. déduc. | 62
BE | 1 | European | 2 | INVES | 0 |  |  |  |  | 19 | Investissement services intracom. | Investissement services intracom. | 63
BE | 1 | European | 2 | INVES | 21 | 1 | DEDUC | true | TRUE | 19 | Investissement services intracom. | Investissement services intracom. | 64
BE | 1 | European | 2 | INVES | 21 | 1 | DEDUC | false | FALSE | 19 | Investissement services intracom. | Investissement services intracom. | 64
BE | 1 | European | 2 | INVES | 21 | 3 | PCT | 35 | 35 % | 27 | Investissement services Intracom. part. déduc. | Investissement services Intracom. part. déduc. | 65
BE | 1 | European | 2 | INVES | 21 | 3 | PCT | 50 | 50 % | 27 | Investissement services Intracom. part. déduc. | Investissement services Intracom. part. déduc. | 65
BE | 1 | European | 2 | INVES | 21 | 3 | PCT | 75 | 75 % | 27 | Investissement services Intracom. part. déduc. | Investissement services Intracom. part. déduc. | 65
BE | 1 | European | 2 | INVES | 21 | 3 | PCT | 85 | 85 % | 27 | Investissement services Intracom. part. déduc. | Investissement services Intracom. part. déduc. | 65
BE | 1 | European | 0 | MERCH | 21 | 0 | COUNTRY |  |  | 26 | Marchandises taxées à l'origine | Marchandises taxées à l'origine | 66
BE | 1 | European | 1 | GS | 21 | 0 | COUNTRY |  |  | 7 | Biens taxés à l'origine | Biens taxés à l'origine | 67
BE | 1 | European | 1 | GS | 21 | 0 | COUNTRY |  |  | 36 | Services taxés à l'origine | Services taxés à l'origine | 68
BE | 1 | European | 2 | INVES | 21 | 0 | COUNTRY |  |  | 21 | Investissements taxés à l'origine | Investissements taxés à l'origine | 69
BE | 1 | European | 0 | MERCH | 21 |  |  |  |  | 37 | Sous-traitance transport/consult. | Sous-traitance transport/consult. | 71
BE | 2 | International | 0 | MERCH | 0 |  |  |  |  | 15 | Import Marchandises | Import Marchandises | 72
BE | 2 | International | 1 | GS | 0 |  |  |  |  | 13 | Import Biens et Services | Import Biens et Services | 73
BE | 2 | International | 2 | INVES | 0 |  |  |  |  | 14 | Import Investissements | Import Investissements | 74
BE | 2 | International | 0 | MERCH | 21 | 1 | DEDUC | true | TRUE | 33 | Report Marchandises | Report Marchandises | 75
BE | 2 | International | 0 | MERCH | 21 | 1 | DEDUC | false | FALSE | 33 | Report Marchandises | Report Marchandises | 75
BE | 2 | International | 0 | MERCH | 21 | 1 | DEDUC | true | TRUE | 34 | Report Marchandises Taxes dues par le preneur | Report Marchandises Taxes dues par le preneur | 76
BE | 2 | International | 0 | MERCH | 21 | 1 | DEDUC | false | FALSE | 34 | Report Marchandises Taxes dues par le preneur | Report Marchandises Taxes dues par le preneur | 76
BE | 2 | International | 1 | GS | 21 | 1 | DEDUC | true | TRUE | 29 | Report Biens et Services | Report Biens et Services | 77
BE | 2 | International | 1 | GS | 21 | 1 | DEDUC | false | FALSE | 29 | Report Biens et Services | Report Biens et Services | 77
BE | 2 | International | 1 | GS | 21 | 1 | DEDUC | true | TRUE | 30 | Report Biens et Services Taxes dues par le preneur | Report Biens et Services Taxes dues par le preneur | 78
BE | 2 | International | 1 | GS | 21 | 1 | DEDUC | false | FALSE | 30 | Report Biens et Services Taxes dues par le preneur | Report Biens et Services Taxes dues par le preneur | 78
BE | 2 | International | 2 | INVES | 21 | 1 | DEDUC | true | TRUE | 31 | Report Investissement | Report Investissement | 79
BE | 2 | International | 2 | INVES | 21 | 1 | DEDUC | false | FALSE | 31 | Report Investissement | Report Investissement | 79
BE | 2 | International | 2 | INVES | 21 | 1 | DEDUC | true | TRUE | 32 | Report Investissement Taxes dues par le preneur | Report Investissement Taxes dues par le preneur | 80
BE | 2 | International | 2 | INVES | 21 | 1 | DEDUC | false | FALSE | 32 | Report Investissement Taxes dues par le preneur | Report Investissement Taxes dues par le preneur | 80
```

### Sheet: Combinations (LU) (146 rows)

```text
Legislation | TaxType | TaxType | TaxKind | TaxKind | TaxRate | TaxCondition | TaxCondition | TaxConditionValue | TaxConditionValue | TaxOrigin | TaxOrigin - FR | TaxOrigin - NL | OrderView (to ignore)
LU | 0 | National | 0 | MERCH | 0 |  |  |  |  | 24 | Marchandises | Marchandises | 122
LU | 0 | National | 0 | MERCH | 3 | 1 | DEDUC | true | TRUE | 24 | Marchandises | Marchandises | 123
LU | 0 | National | 0 | MERCH | 3 | 1 | DEDUC | false | FALSE | 24 | Marchandises | Marchandises | 123
LU | 0 | National | 0 | MERCH | 7 | 1 | DEDUC | true | TRUE | 24 | Marchandises | Marchandises | 124
LU | 0 | National | 0 | MERCH | 7 | 1 | DEDUC | false | FALSE | 24 | Marchandises | Marchandises | 124
LU | 0 | National | 0 | MERCH | 8 | 1 | DEDUC | true | TRUE | 24 | Marchandises | Marchandises | 124
LU | 0 | National | 0 | MERCH | 8 | 1 | DEDUC | false | FALSE | 24 | Marchandises | Marchandises | 124
LU | 0 | National | 0 | MERCH | 13 | 1 | DEDUC | true | TRUE | 24 | Marchandises | Marchandises | 125
LU | 0 | National | 0 | MERCH | 13 | 1 | DEDUC | false | FALSE | 24 | Marchandises | Marchandises | 125
LU | 0 | National | 0 | MERCH | 14 | 1 | DEDUC | true | TRUE | 24 | Marchandises | Marchandises | 125
LU | 0 | National | 0 | MERCH | 14 | 1 | DEDUC | false | FALSE | 24 | Marchandises | Marchandises | 125
LU | 0 | National | 0 | MERCH | 16 | 1 | DEDUC | true | TRUE | 24 | Marchandises | Marchandises | 126
LU | 0 | National | 0 | MERCH | 16 | 1 | DEDUC | false | FALSE | 24 | Marchandises | Marchandises | 126
LU | 0 | National | 0 | MERCH | 17 | 1 | DEDUC | true | TRUE | 24 | Marchandises | Marchandises | 126
LU | 0 | National | 0 | MERCH | 17 | 1 | DEDUC | false | FALSE | 24 | Marchandises | Marchandises | 126
LU | 0 | National | 1 | GS | 0 |  |  |  |  | 11 | Frais généraux | Frais généraux | 127
LU | 0 | National | 1 | GS | 3 | 1 | DEDUC | true | TRUE | 11 | Frais généraux | Frais généraux | 128
LU | 0 | National | 1 | GS | 3 | 1 | DEDUC | false | FALSE | 11 | Frais généraux | Frais généraux | 128
LU | 0 | National | 1 | GS | 7 | 1 | DEDUC | true | TRUE | 11 | Frais généraux | Frais généraux | 129
LU | 0 | National | 1 | GS | 7 | 1 | DEDUC | false | FALSE | 11 | Frais généraux | Frais généraux | 129
LU | 0 | National | 1 | GS | 8 | 1 | DEDUC | true | TRUE | 11 | Frais généraux | Frais généraux | 129
LU | 0 | National | 1 | GS | 8 | 1 | DEDUC | false | FALSE | 11 | Frais généraux | Frais généraux | 129
LU | 0 | National | 1 | GS | 13 | 1 | DEDUC | true | TRUE | 11 | Frais généraux | Frais généraux | 130
LU | 0 | National | 1 | GS | 13 | 1 | DEDUC | false | FALSE | 11 | Frais généraux | Frais généraux | 130
LU | 0 | National | 1 | GS | 14 | 1 | DEDUC | true | TRUE | 11 | Frais généraux | Frais généraux | 130
LU | 0 | National | 1 | GS | 14 | 1 | DEDUC | false | FALSE | 11 | Frais généraux | Frais généraux | 130
LU | 0 | National | 1 | GS | 16 | 1 | DEDUC | true | TRUE | 11 | Frais généraux | Frais généraux | 131
LU | 0 | National | 1 | GS | 16 | 1 | DEDUC | false | FALSE | 11 | Frais généraux | Frais généraux | 131
LU | 0 | National | 1 | GS | 17 | 1 | DEDUC | true | TRUE | 11 | Frais généraux | Frais généraux | 131
LU | 0 | National | 1 | GS | 17 | 1 | DEDUC | false | FALSE | 11 | Frais généraux | Frais généraux | 131
LU | 0 | National | 2 | INVES | 3 | 1 | DEDUC | true | TRUE | 20 | Investissements | Investissements | 132
LU | 0 | National | 2 | INVES | 3 | 1 | DEDUC | false | FALSE | 20 | Investissements | Investissements | 132
LU | 0 | National | 2 | INVES | 7 | 1 | DEDUC | true | TRUE | 20 | Investissements | Investissements | 133
LU | 0 | National | 2 | INVES | 7 | 1 | DEDUC | false | FALSE | 20 | Investissements | Investissements | 133
LU | 0 | National | 2 | INVES | 8 | 1 | DEDUC | true | TRUE | 20 | Investissements | Investissements | 133
LU | 0 | National | 2 | INVES | 8 | 1 | DEDUC | false | FALSE | 20 | Investissements | Investissements | 133
LU | 0 | National | 2 | INVES | 13 | 1 | DEDUC | true | TRUE | 20 | Investissements | Investissements | 134
LU | 0 | National | 2 | INVES | 13 | 1 | DEDUC | false | FALSE | 20 | Investissements | Investissements | 134
LU | 0 | National | 2 | INVES | 14 | 1 | DEDUC | true | TRUE | 20 | Investissements | Investissements | 134
LU | 0 | National | 2 | INVES | 14 | 1 | DEDUC | false | FALSE | 20 | Investissements | Investissements | 134
LU | 0 | National | 2 | INVES | 16 | 1 | DEDUC | true | TRUE | 20 | Investissements | Investissements | 135
LU | 0 | National | 2 | INVES | 16 | 1 | DEDUC | false | FALSE | 20 | Investissements | Investissements | 135
LU | 0 | National | 2 | INVES | 17 | 1 | DEDUC | true | TRUE | 20 | Investissements | Investissements | 135
LU | 0 | National | 2 | INVES | 17 | 1 | DEDUC | false | FALSE | 20 | Investissements | Investissements | 135
LU | 0 | National | 0 | MERCH | 0 |  |  |  |  | 3 | Achats de tabacs | Achats de tabacs | 136
LU | 1 | European | 0 | MERCH | 0 |  |  |  |  | 40 | UE - Marchandises - Biens | UE - Marchandises - Biens | 137
LU | 1 | European | 0 | MERCH | 0 |  |  |  |  | 41 | UE - Marchandises - Biens - triangulaire | UE - Marchandises - Biens - triangulaire | 138
LU | 1 | European | 0 | MERCH | 3 |  |  |  |  | 40 | UE - Marchandises - Biens | UE - Marchandises - Biens | 139
LU | 1 | European | 0 | MERCH | 7 |  |  |  |  | 40 | UE - Marchandises - Biens | UE - Marchandises - Biens | 140
LU | 1 | European | 0 | MERCH | 8 |  |  |  |  | 40 | UE - Marchandises - Biens | UE - Marchandises - Biens | 140
LU | 1 | European | 0 | MERCH | 13 |  |  |  |  | 40 | UE - Marchandises - Biens | UE - Marchandises - Biens | 141
LU | 1 | European | 0 | MERCH | 14 |  |  |  |  | 40 | UE - Marchandises - Biens | UE - Marchandises - Biens | 141
LU | 1 | European | 0 | MERCH | 16 |  |  |  |  | 40 | UE - Marchandises - Biens | UE - Marchandises - Biens | 142
LU | 1 | European | 0 | MERCH | 17 |  |  |  |  | 40 | UE - Marchandises - Biens | UE - Marchandises - Biens | 142
LU | 1 | European | 0 | MERCH | 0 |  |  |  |  | 42 | UE - Marchandises - Services | UE - Marchandises - Services | 143
LU | 1 | European | 0 | MERCH | 3 |  |  |  |  | 42 | UE - Marchandises - Services | UE - Marchandises - Services | 144
LU | 1 | European | 0 | MERCH | 7 |  |  |  |  | 42 | UE - Marchandises - Services | UE - Marchandises - Services | 145
LU | 1 | European | 0 | MERCH | 8 |  |  |  |  | 42 | UE - Marchandises - Services | UE - Marchandises - Services | 145
LU | 1 | European | 0 | MERCH | 13 |  |  |  |  | 42 | UE - Marchandises - Services | UE - Marchandises - Services | 146
LU | 1 | European | 0 | MERCH | 14 |  |  |  |  | 42 | UE - Marchandises - Services | UE - Marchandises - Services | 146
LU | 1 | European | 0 | MERCH | 16 |  |  |  |  | 42 | UE - Marchandises - Services | UE - Marchandises - Services | 147
LU | 1 | European | 0 | MERCH | 17 |  |  |  |  | 42 | UE - Marchandises - Services | UE - Marchandises - Services | 147
LU | 1 | European | 1 | GS | 0 |  |  |  |  | 43 | UE - Frais généraux - Biens | UE - Frais généraux - Biens | 148
LU | 1 | European | 1 | GS | XX | 0 | COUNTRY | XX (= CountryCode) |  | 44 | UE - Frais généraux - Biens - taxation origine | UE - Frais généraux - Biens - taxation origine | 149
LU | 1 | European | 1 | GS | 3 |  |  |  |  | 43 | UE - Frais généraux - Biens | UE - Frais généraux - Biens | 150
LU | 1 | European | 1 | GS | 7 |  |  |  |  | 43 | UE - Frais généraux - Biens | UE - Frais généraux - Biens | 151
LU | 1 | European | 1 | GS | 8 |  |  |  |  | 43 | UE - Frais généraux - Biens | UE - Frais généraux - Biens | 151
LU | 1 | European | 1 | GS | 13 |  |  |  |  | 43 | UE - Frais généraux - Biens | UE - Frais généraux - Biens | 152
LU | 1 | European | 1 | GS | 14 |  |  |  |  | 43 | UE - Frais généraux - Biens | UE - Frais généraux - Biens | 152
LU | 1 | European | 1 | GS | 16 |  |  |  |  | 43 | UE - Frais généraux - Biens | UE - Frais généraux - Biens | 153
LU | 1 | European | 1 | GS | 17 |  |  |  |  | 43 | UE - Frais généraux - Biens | UE - Frais généraux - Biens | 153
LU | 1 | European | 2 | INVES | 0 |  |  |  |  | 45 | UE - Investissements - Biens | UE - Investissements - Biens | 154
LU | 1 | European | 2 | INVES | 3 |  |  |  |  | 45 | UE - Investissements - Biens | UE - Investissements - Biens | 155
LU | 1 | European | 2 | INVES | 7 |  |  |  |  | 45 | UE - Investissements - Biens | UE - Investissements - Biens | 156
LU | 1 | European | 2 | INVES | 8 |  |  |  |  | 45 | UE - Investissements - Biens | UE - Investissements - Biens | 156
LU | 1 | European | 2 | INVES | 13 |  |  |  |  | 45 | UE - Investissements - Biens | UE - Investissements - Biens | 157
LU | 1 | European | 2 | INVES | 14 |  |  |  |  | 45 | UE - Investissements - Biens | UE - Investissements - Biens | 157
LU | 1 | European | 2 | INVES | 16 |  |  |  |  | 45 | UE - Investissements - Biens | UE - Investissements - Biens | 158
LU | 1 | European | 2 | INVES | 17 |  |  |  |  | 45 | UE - Investissements - Biens | UE - Investissements - Biens | 158
LU | 1 | European | 2 | INVES | 0 |  |  |  |  | 46 | UE - Investissements - Services | UE - Investissements - Services | 159
LU | 1 | European | 2 | INVES | 3 |  |  |  |  | 46 | UE - Investissements - Services | UE - Investissements - Services | 160
LU | 1 | European | 2 | INVES | 7 |  |  |  |  | 46 | UE - Investissements - Services | UE - Investissements - Services | 161
LU | 1 | European | 2 | INVES | 8 |  |  |  |  | 46 | UE - Investissements - Services | UE - Investissements - Services | 161
LU | 1 | European | 2 | INVES | 13 |  |  |  |  | 46 | UE - Investissements - Services | UE - Investissements - Services | 162
LU | 1 | European | 2 | INVES | 14 |  |  |  |  | 46 | UE - Investissements - Services | UE - Investissements - Services | 162
LU | 1 | European | 2 | INVES | 16 |  |  |  |  | 46 | UE - Investissements - Services | UE - Investissements - Services | 163
LU | 1 | European | 2 | INVES | 17 |  |  |  |  | 46 | UE - Investissements - Services | UE - Investissements - Services | 163
LU | 1 | European | 0 | MERCH | 0 |  |  |  |  | 47 | UE - Achats de tabacs | UE - Achats de tabacs | 164
LU | 1 | European | 1 | GS | 0 |  |  |  |  | 48 | UE - Frais généraux - Services | UE - Frais généraux - Services | 165
LU | 1 | European | 1 | GS | XX | 0 | COUNTRY | XX (= CountryCode) |  | 49 | UE - Frais généraux - Services - taxation origine | UE - Frais généraux - Services - taxation origine | 166
LU | 1 | European | 1 | GS | 3 |  |  |  |  | 48 | UE - Frais généraux - Services | UE - Frais généraux - Services | 167
LU | 1 | European | 1 | GS | 7 |  |  |  |  | 48 | UE - Frais généraux - Services | UE - Frais généraux - Services | 168
LU | 1 | European | 1 | GS | 8 |  |  |  |  | 48 | UE - Frais généraux - Services | UE - Frais généraux - Services | 168
LU | 1 | European | 1 | GS | 13 |  |  |  |  | 48 | UE - Frais généraux - Services | UE - Frais généraux - Services | 169
LU | 1 | European | 1 | GS | 14 |  |  |  |  | 48 | UE - Frais généraux - Services | UE - Frais généraux - Services | 169
LU | 1 | European | 1 | GS | 16 |  |  |  |  | 48 | UE - Frais généraux - Services | UE - Frais généraux - Services | 170
LU | 1 | European | 1 | GS | 17 |  |  |  |  | 48 | UE - Frais généraux - Services | UE - Frais généraux - Services | 170
LU | 2 | International | 0 | MERCH | 0 |  |  |  |  | 50 | Import - Marchandises - Biens | Import - Marchandises - Biens | 171
LU | 2 | International | 0 | MERCH | 3 |  |  |  |  | 50 | Import - Marchandises - Biens | Import - Marchandises - Biens | 172
LU | 2 | International | 0 | MERCH | 7 |  |  |  |  | 50 | Import - Marchandises - Biens | Import - Marchandises - Biens | 173
LU | 2 | International | 0 | MERCH | 8 |  |  |  |  | 50 | Import - Marchandises - Biens | Import - Marchandises - Biens | 173
LU | 2 | International | 0 | MERCH | 13 |  |  |  |  | 50 | Import - Marchandises - Biens | Import - Marchandises - Biens | 174
LU | 2 | International | 0 | MERCH | 14 |  |  |  |  | 50 | Import - Marchandises - Biens | Import - Marchandises - Biens | 174
LU | 2 | International | 0 | MERCH | 16 |  |  |  |  | 50 | Import - Marchandises - Biens | Import - Marchandises - Biens | 175
LU | 2 | International | 0 | MERCH | 17 |  |  |  |  | 50 | Import - Marchandises - Biens | Import - Marchandises - Biens | 175
LU | 2 | International | 0 | MERCH | 0 |  |  |  |  | 51 | Import - Marchandises - Services | Import - Marchandises - Services | 176
LU | 2 | International | 0 | MERCH | 3 |  |  |  |  | 51 | Import - Marchandises - Services | Import - Marchandises - Services | 177
LU | 2 | International | 0 | MERCH | 7 |  |  |  |  | 51 | Import - Marchandises - Services | Import - Marchandises - Services | 178
LU | 2 | International | 0 | MERCH | 8 |  |  |  |  | 51 | Import - Marchandises - Services | Import - Marchandises - Services | 178
LU | 2 | International | 0 | MERCH | 13 |  |  |  |  | 51 | Import - Marchandises - Services | Import - Marchandises - Services | 179
LU | 2 | International | 0 | MERCH | 14 |  |  |  |  | 51 | Import - Marchandises - Services | Import - Marchandises - Services | 179
LU | 2 | International | 0 | MERCH | 16 |  |  |  |  | 51 | Import - Marchandises - Services | Import - Marchandises - Services | 180
LU | 2 | International | 0 | MERCH | 17 |  |  |  |  | 51 | Import - Marchandises - Services | Import - Marchandises - Services | 180
LU | 2 | International | 0 | MERCH | 0 |  |  |  |  | 52 | Import - Achats de tabacs | Import - Achats de tabacs | 181
LU | 2 | International | 1 | GS | 0 |  |  |  |  | 53 | Import - Frais généraux - Biens | Import - Frais généraux - Biens | 182
LU | 2 | International | 1 | GS | 3 |  |  |  |  | 53 | Import - Frais généraux - Biens | Import - Frais généraux - Biens | 183
LU | 2 | International | 1 | GS | 7 |  |  |  |  | 53 | Import - Frais généraux - Biens | Import - Frais généraux - Biens | 184
LU | 2 | International | 1 | GS | 8 |  |  |  |  | 53 | Import - Frais généraux - Biens | Import - Frais généraux - Biens | 184
LU | 2 | International | 1 | GS | 13 |  |  |  |  | 53 | Import - Frais généraux - Biens | Import - Frais généraux - Biens | 185
LU | 2 | International | 1 | GS | 14 |  |  |  |  | 53 | Import - Frais généraux - Biens | Import - Frais généraux - Biens | 185
LU | 2 | International | 1 | GS | 16 |  |  |  |  | 53 | Import - Frais généraux - Biens | Import - Frais généraux - Biens | 186
LU | 2 | International | 1 | GS | 17 |  |  |  |  | 53 | Import - Frais généraux - Biens | Import - Frais généraux - Biens | 186
LU | 2 | International | 1 | GS | 0 |  |  |  |  | 54 | Import - Frais généraux - Services | Import - Frais généraux - Services | 187
LU | 2 | International | 1 | GS | 3 |  |  |  |  | 54 | Import - Frais généraux - Services | Import - Frais généraux - Services | 188
LU | 2 | International | 1 | GS | 7 |  |  |  |  | 54 | Import - Frais généraux - Services | Import - Frais généraux - Services | 189
LU | 2 | International | 1 | GS | 8 |  |  |  |  | 54 | Import - Frais généraux - Services | Import - Frais généraux - Services | 189
LU | 2 | International | 1 | GS | 13 |  |  |  |  | 54 | Import - Frais généraux - Services | Import - Frais généraux - Services | 190
LU | 2 | International | 1 | GS | 14 |  |  |  |  | 54 | Import - Frais généraux - Services | Import - Frais généraux - Services | 190
LU | 2 | International | 1 | GS | 16 |  |  |  |  | 54 | Import - Frais généraux - Services | Import - Frais généraux - Services | 191
LU | 2 | International | 1 | GS | 17 |  |  |  |  | 54 | Import - Frais généraux - Services | Import - Frais généraux - Services | 191
LU | 2 | International | 2 | INVES | 0 |  |  |  |  | 55 | Import - Investissements - Biens | Import - Investissements - Biens | 192
LU | 2 | International | 2 | INVES | 3 |  |  |  |  | 55 | Import - Investissements - Biens | Import - Investissements - Biens | 193
LU | 2 | International | 2 | INVES | 7 |  |  |  |  | 55 | Import - Investissements - Biens | Import - Investissements - Biens | 194
LU | 2 | International | 2 | INVES | 8 |  |  |  |  | 55 | Import - Investissements - Biens | Import - Investissements - Biens | 194
LU | 2 | International | 2 | INVES | 13 |  |  |  |  | 55 | Import - Investissements - Biens | Import - Investissements - Biens | 195
LU | 2 | International | 2 | INVES | 14 |  |  |  |  | 55 | Import - Investissements - Biens | Import - Investissements - Biens | 195
LU | 2 | International | 2 | INVES | 16 |  |  |  |  | 55 | Import - Investissements - Biens | Import - Investissements - Biens | 196
LU | 2 | International | 2 | INVES | 17 |  |  |  |  | 55 | Import - Investissements - Biens | Import - Investissements - Biens | 196
LU | 2 | International | 2 | INVES | 0 |  |  |  |  | 56 | Import - Investissements - Services | Import - Investissements - Services | 197
LU | 2 | International | 2 | INVES | 3 |  |  |  |  | 56 | Import - Investissements - Services | Import - Investissements - Services | 198
LU | 2 | International | 2 | INVES | 7 |  |  |  |  | 56 | Import - Investissements - Services | Import - Investissements - Services | 199
LU | 2 | International | 2 | INVES | 8 |  |  |  |  | 56 | Import - Investissements - Services | Import - Investissements - Services | 199
LU | 2 | International | 2 | INVES | 13 |  |  |  |  | 56 | Import - Investissements - Services | Import - Investissements - Services | 200
LU | 2 | International | 2 | INVES | 14 |  |  |  |  | 56 | Import - Investissements - Services | Import - Investissements - Services | 200
LU | 2 | International | 2 | INVES | 16 |  |  |  |  | 56 | Import - Investissements - Services | Import - Investissements - Services | 201
LU | 2 | International | 2 | INVES | 17 |  |  |  |  | 56 | Import - Investissements - Services | Import - Investissements - Services | 201
```

### Sheet: Available values (36 rows)

```text
 |  |  |  |  | TaxOrigin (BE) |  |  |  | TaxOrigin (LU)
 |  |  |  |  | 0 | Achat Biens et Services |  |  | 3 | Achats de tabacs
 | TaxKind |  |  |  | 1 | Achat Investissements |  |  | 11 | Frais généraux
 | NULL | - |  |  | 2 | Achat Marchandises |  |  | 20 | Investissements
 | 0 | MERCH |  |  | 4 | Autres exemptions |  |  | 24 | Marchandises
 | 1 | GS (Goods and services) |  |  | 5 | Autres exemptions avec MAJ du C.A. |  |  | 40 | UE - Marchandises - Biens
 | 2 | INVES |  |  | 6 | Biens Intracommunautaires |  |  | 41 | UE - Marchandises - Biens - triangulaire
 |  |  |  |  | 7 | Biens taxés à l'origine |  |  | 42 | UE - Marchandises - Services
 | TaxCondition |  |  |  | 8 | Cocontractant immobilier |  |  | 43 | UE - Frais généraux - Biens
 | NULL | - |  |  | 9 | Escompte |  |  | 44 | UE - Frais généraux - Biens - taxation origine
 | 0 | COUNTRY |  |  | 10 | Frais de voiture / Multimédia |  |  | 45 | UE - Investissements - Biens
 | 1 | DEDUC |  |  | 13 | Import Biens et Services |  |  | 46 | UE - Investissements - Services
 | 2 | INVEST |  |  | 14 | Import Investissements |  |  | 47 | UE - Achats de tabacs
 | 3 | PCT |  |  | 15 | Import Marchandises |  |  | 48 | UE - Frais généraux - Services
 |  |  |  |  | 17 | Investissement biens Intracom. |  |  | 49 | UE - Frais généraux - Services - taxation origine
 | TaxConditionValue |  |  |  | 18 | Investissement partiellement récupérable |  |  | 50 | Import - Marchandises - Biens
 | (Condition: DEDUC / INVEST) |  |  |  | 19 | Investissement services intracom. |  |  | 51 | Import - Marchandises - Services
 | true | TRUE |  |  | 21 | Investissements taxés à l'origine |  |  | 52 | Import - Achats de tabacs
 | false | FALSE |  |  | 25 | Marchandises Intracommunautaires |  |  | 53 | Import - Frais généraux - Biens
 |  |  |  |  | 26 | Marchandises taxées à l'origine |  |  | 54 | Import - Frais généraux - Services
 |  |  |  |  | 28 | Prestations de sous-traitance |  |  | 55 | Import - Investissements - Biens
 |  |  |  |  | 29 | Report Biens et Services |  |  | 56 | Import - Investissements - Services
 | TaxConditionValue |  |  |  | 30 | Report Biens et Services Taxes dues par le preneur
 | (Condition: PCT) |  |  |  | 31 | Report Investissement
 | 35 | 0.35 |  |  | 32 | Report Investissement Taxes dues par le preneur
 | 50 | 0.5 |  |  | 33 | Report Marchandises
 | 75 | 0.75 |  |  | 34 | Report Marchandises Taxes dues par le preneur
 | 85 | 0.85 |  |  | 35 | Services Intracommunautaires
 |  |  |  |  | 36 | Services taxés à l'origine
 |  |  |  |  | 37 | Sous-traitance transport/consult.
 |  |  |  |  | 39 | Vidanges-Emballages
 |  |  |  |  | 12 | Achat TVA Marge
 |  |  |  |  | 16 | Biens Intracom. part. déduc.
 |  |  |  |  | 22 | Services Intracom. part. déduc.
 |  |  |  |  | 23 | Investissement biens Intracom. part. déduc.
 |  |  |  |  | 27 | Investissement services Intracom. part. déduc.
```

