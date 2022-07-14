# Tool-for-Aborea
## This tool functions are:

1. Characktererstellung
Die Charaktererstellung funktioniert nach dem einfachen Prinzip füll alles aus, ab  dann ist es speicherbar. Lediglich die Fertigkeiten sind keine plichtfelder.

2. Laden und Löschen von Charaktere
Die erstellten charaktere werden in einem unterordner erstellt und von dort aus geladen.

## Wichtige Notizen!

### Klassen

Um mehr Klassen hinzuzufügen, muss die Datein 'klassen.txt' bearbeitet werden. Dabei kann die gewünschte Klasse unten engefügt werden und zwas im Format 

**NAME BERECHNUNG-LEBEN BERECHNUNG-MANA KOSTEN-F1 KOSTEN-F2 ... KOSTEN-FN**

- NAME              
  - Name der Klasse
  - Beispiel: Krieger
- BERECHNUNG-LEBEN
  - Im Format XA, hierbei steht X für den Bonus fürs Leben und A für das Attribut, welches bei der Berechnung eine Rolle spielt (Standardmäßig  Konstitution)
  - Wichtig: kleiner Buchstabe und nur 1-Ziffer-lang
  - Beispiel: 10k
- BERECHNUNG-MANA
  - Im Format XA, hierbei steht X für den Bonus fürs Mana und A für das Attribut, welches bei der Berechnung eine Rolle spielt (Standardmäßig Intelligenz oder Charisma)
  - Wichtig: kleiner Buchstabe und nur 1-Ziffer-lang
  - Beispiel: 3i
- KOSTEN-F1
  - Kosten der 1. Fertigkeit aus der Datein 'Fertigkeiten'("von oben nach unten"), im Format von X oder X&Y.
  - 1. Beispiel: 2
  - 2. Beispiel: 2&3
- KOSTEN-F2
  - Kosten der 2. Fertigkeit aus der Datein 'Fertigkeiten'("von oben nach unten"), im Format von X oder X&Y.
  - 1. Beispiel: 1
  - 2. Beispiel: 2&4   

.

.

.

                      
- KOSTEN-FN
  - Kosten der Nten Fertigkeit aus der Datein 'Fertigkeiten'("von oben nach unten"), im Format von X oder X&Y.
  - 1. Beispiel: 4
  - 2. Beispiel: 1&3

### Fertigkeiten

In der Datei 'fertigkeiten.txt' sind die Fertigkeiten untereinander aufgeführt.
Sollte eine Fertigkeit hinzugefügt werden, dann müssen die Kosten in jeder Klasse aktualisiert werden. Dazu mehr unter dem Kapitel Klassen.

### Völker

In der Datei 'voelker.txt' befinden sich alle voelker unter einander im Format:

**NAME LEBENS-BONUS STÄRKE-BONUS GESCHICKLICHKEITS-BONUS KONSTITUTIONS-BONUS INTELLIGENZ-BONUS CHARISMA-BONUS**

- NAME
  - Name des Volkes
- LEBENS-BONUS
  - Bonus für die Lebensberechnung, im Format LX (L steht für Leben und X für ein Wert)
  - Dieser Wert sollte, wenn Möglich >= 0 sein, da unter umständen sonst Leben von <= 0 möglich wäre.
  - Beispiel: L2 (Zwerge)
- GESCHICKLICHKEITS-BONUS
  - Bonus für das Attribut Geschicklichkeit bei der Charakter erstellung, im Format X.
  - Beispiel: 2
- KONSTITUTIONS-BONUS
  - Bonus für das Attribut Konstitution bei der Charakter erstellung, im Format X.
  - Beispiel: 1
- INTELLIGENZ-BONUS
  - Bonus für das Attribut Intelligenz bei der Charakter erstellung, im Format X.
  - Beispiel: -2
- CHARISMA-BONUS
  - Bonus für das Attribut Charisma bei der Charakter erstellung, im Format X.
  - Beispiel: -1
                            
Bei den verschiedenen Attributs-Boni sollte darauf geachtet werden, dass deren Gesamtsumme möglichst = 0 ist, um ausgeglichene Völker zuhaben. Dies ist jedoch nur ein Richtwert.

                        
