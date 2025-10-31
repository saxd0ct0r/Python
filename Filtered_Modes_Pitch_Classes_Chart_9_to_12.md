# Filtered Modes Pitch Classes Chart (PCs 9–12, Minimum 3 PCs)

| Collection   | Mode             | PC 0  | PC 1  | PC 2  | PC 3  | PC 4  | PC 5  | PC 6  | PC 7  | PC 8  | PC 9  | PC10  | PC11  | PC12  | Sec. Mode        | Weighting     |
|:-------------|:-----------------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:-----------------|:--------------|
| Major        | Lydian           | xxx | xxx | xxx | xxx | xxx | xxx | xxx | xxx | xxx | Re  |     | Mi  | Fa  | Dorian           | 9999999991223 |
| Major        | Mixolydian       | xxx | xxx | xxx | xxx | xxx | xxx | xxx | xxx | xxx | Mi  | Fa  |     | Sol | Phrygian         | 9999999991123 |

**Notes:**
- Filtered for modes with at least 3 pitch classes in the range PCs 9–12. Non-included columns (0–8) are obscured with 'xxx'.
- For duplicate weighting function values, retains the mode with the highest priority based on collection priority (Major > H Minor > M Minor > H Major > Diminished > WT > Tritone > Augmented > Maj triad > Min triad > Maj7 > Dom7 > Min7 > Min7b5 > Dim7), then Secondary Mode priority within the collection.
- Pitch classes (0–12) show the solfege syllable if present in the mode, relative to the mode's root as pitch class 0; empty if not present. PC 12 doubles the octave.
- Secondary Mode is the mode from the same parent collection whose solfege sequence, starting from its root, matches the solfege syllables in PCs 9–12 in order. For start_column=0 in non-symmetric collections, the Secondary Mode is 'None' if it would be the same mode.
- Solfege is fixed relative to the parent scale or chord's tonic: Major (Do as Ionian root), H Minor (La as Aeolian ♯7 root, with Si as raised 7th), M Minor (Re as Dorian ♯7 root, with Di as raised 7th), H Major (Do as Ionian ♭6 root, with Le as lowered 6th), Diminished (Ti as Diminished ♮9 root, with Di, Le, Li as chromatic alterations), WT (Fa as Whole-Tone root, with Di and Ri as chromatic alterations), Tritone (Di as Tritone ♭9 root, with Di, Re, Fa, Sol, Le, Ti), Maj triad/Maj7 (Do as root), Min triad/Min7 (Re as root), Dom7 (Sol as root), Min7b5 (Ti as root), Dim7 (Si as root, with Si, Ti, Re, Fa), Augmented (Ti as Augmented ♭9 root, with Ti, Do, Ri, Mi, Sol, Le).
- Weighting Function is a 13-digit integer prioritizing density towards higher pitch classes in the range 9–12, with left-most digit as count of PC 12, next as PCs 9–12, ..., padded left with 9s to maintain 13 digits.
- Chord inversions are named as triad/3 (1st inversion), triad/5 (2nd inversion) for triads, and chord/3, chord/5, chord/7 for seventh chords.
- Tritone scale is a hexachord [0, 1, 4, 6, 7, 10], a composite of two major triads a tritone apart, with modes named ♭9 (first interval half step), ♮9 (whole step), ♯9 (minor third).
- Augmented scale is a hexachord [0, 1, 4, 5, 8, 9], a composite of two augmented triads a half step apart or three major triads a major third apart with one shared pitch each, with modes named ♭9 (first interval half step) or ♯9 (minor third).
