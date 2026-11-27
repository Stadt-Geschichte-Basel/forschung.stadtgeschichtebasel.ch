---
title: Daten
layout: page
permalink: /data.html
---

# Daten

<div>{% include data-download-cards.html %}</div>

## Datenmodell

### Annotation

Metadaten für die auf der Forschungsdatenplattform vorgestellten Elemente werden gemäss einem Datenmodell bereitgestellt, das vom Team für Forschungdatenmanagement der Stadt.Geschichte.Basel entwickelt wurde, um den Anforderungen der vielfältigen im Projekt verwendeten Quellen gerecht zu werden. Das Datenmodell (und der anschliessende Annotationsprozess) für die Forschungsdaten aus den neun publizierten Bänden folgen dem [Handbuch zur Erstellung diskriminerungsfreier Metadaten für historische Quellen und Forschungsdaten](https://maehr.github.io/diskriminierungsfreie-metadaten/){:target="\_blank"}, das ebenfalls von Stadt.Geschichte.Basel entwickelt wurde.

Zusätzlich zu den Daten aus den neun Büchern sind auf der Forschungsdatenplattform auch Inhalte aus weiteren im Projekt entstandenen Veröffentlichungen verfügbar, darunter statische Versionen der interaktiven Data Stories inklusive der verwendeten Medienobjekte. Metadaten für diese Objekte, die nicht Teil der neun Bände der Stadt.Geschichte.Basel sind, wurden mit KI-Unterstützung erstellt.

Das Datenmodell enthält kein `subject`-Feld. Stadt.Geschichte.Basel hat beschlossen, seinen Forschungsdaten keine thematischen Schlagwörter zuzuordnen. Diese Entscheidung ist auf [GitHub](https://github.com/Stadt-Geschichte-Basel/stadt-geschichte-basel.github.io/issues/104) dokumentiert.

### Identifikatoren

Alle Objekte auf der Plattform haben einen eindeutigen Identifkator. Die Annotation der Forschungsdaten, die Teil der Buchpublikationen sind, ist so konzipiert, dass jedes Metadatenobjekt eine fünfstellige Zahl zugewiesen bekommt, die mit dem Präfix `abb` als Identifikator fungiert, z.B. `abb01313`. Dieses Metadatenobjekt enthält ein oder mehrere untergeordnete Medienobjekte mit eigenen Identifikatoren, jeweils mit dem Präfix `m`. Dabei verwenden beide Objekttypen dieselbe fünfstellige Zahl nach dem Präfix, also z.B. `m01313` für `abb01313`. Wenn ein Metadatenobjekt mehr als ein untergeordnetes Medienobjekt hat, werden die Identifkatoren der untergeordneten Objekte um eine fortlaufende Nummerierung ergänzt: `m01313_1`, `m01313_2` usw.

Für die nicht aus den neun Bänden stammenden Datensätze wurden abweichende Identifikatoren vergeben, dies betrifft hauptsächlich die Data Stories und mit ihnen verbundende Inhalte. Die Data Stories als solche erhalten IDs nach dem Schema `ds-[Titel]` für das Metadatenobjekt der Data Story und `m-[Titel]` für das jeweils untergeordnete Medienobjekt. Die Medien aus den Data Stories erhalten dementsprechend Identifikatoren nach dem Muster `ds-[Titel]-[n]` und `m-[Titel]_[n]`.

Die folgende Grafik veranschaulicht das Datenmodell mit Metadatenfeldern für ein Beispiel-Metadatenobjekt `abb01313`, das ein untergeordnetes Medienobjekt `m01313` hat.

![Datenmodell](assets/img/sgb_datamodel.svg){:style="max-width: 70%; display: block; margin: auto;"}

### EDTF

Das [Extended Date Time Format (EDTF)](https://www.loc.gov/standards/datetime/){:target="\_blank"} ist ein auf [ISO 8601](https://www.iso.org/iso-8601-date-and-time-format.html){:target="\_blank"} aufbauender Standard, der über einfache Datumsangaben hinausgeht und es ermöglicht, komplexe, unsichere, ungefähre oder mehrdeutige Zeitangaben strukturiert und maschinenlesbar festzuhalten. Die wichtigsten Funktionalitäten und Merkmale sind:

1. **Einfache Datumsangaben**  
   Wie bei ISO 8601 üblich, kann man präzise Daten im Format `YYYY-MM-DD` angeben, z. B. `2024-12-11` für den 11. Dezember 2024.  
   Ebenfalls möglich sind Teilangaben wie `2024-12` (Dezember 2024) oder nur das Jahr `2024`.
2. **Ungewisse und ungefähre Daten**  
   Mit speziellen Zeichen lässt sich angeben, wenn ein Datum nur ungefähr oder unsicher ist:

   - `?` kennzeichnet Unsicherheit (z. B. `1960?` könnte bedeuten, dass es etwa 1960 war, aber nicht sicher ist).
   - `~` steht für ungefähre oder in etwa zutreffende Angaben (z. B. `1960~` bedeutet „ungefähr im Jahr 1960“).
   - `%` steht für unsicher und ungefähr

3. **Datumsbereiche und Intervalle**  
   Man kann Zeiträume als Intervalle ausdrücken, indem man zwei Daten mit einem Schrägstrich `/` verbindet:

   - `1900/1950` steht für die Zeitspanne von 1900 bis 1950.
   - Unvollständige Intervalle wie `1900/..` oder `../1950` drücken offene Zeiträume aus („seit 1900“ oder „bis 1950“).
   - Diese Intervalle können ebenfalls Unsicherheits- oder Ungefähr-Zeichen enthalten, um vage Zeiträume darzustellen: `1900~/1950?`.

4. **Listen und Sets von Daten**  
   Man kann mehrere mögliche oder relevante Daten in einer Liste angeben:

   - Eine Liste wie `[1960, 1962, 1965]` bedeutet eine explizite Aufzählung von möglichen oder relevanten Daten.

5. **Jahreszeiten und Quartale**  
   EDTF erlaubt die Angabe von Jahreszeiten oder Quartalen, die in manchen Zusammenhängen relevant sein können:

   - `1960-33` stellt beispielsweise die Angabe „Erstes Quartal des Jahres 1960“ dar.
   - Die Jahreszeiten Frühling, Sommer, Herbst und Winter sind mit den Codes `21`, `22`, `23` und `24` definiert, so kann beispielsweise „Frühling 1960“ mit `1960-21` abgebildet werden.
   - Die genauen Entsprechungen von Zeiten und Codes ist in der Spezifikation des EDTF-Standards festgelegt, um diese einheitlich anzugeben.

6. **Jahrhunderte, Jahrzehnte und unvollständige Angaben**  
   Statt eines konkreten Jahres kann man ganze Jahrzehnte oder Jahrhunderte angeben:
   - `19xx` für ein unbekanntes Jahr im 20. Jahrhundert.
   - `19xx?` für ein ungefähres oder unsicheres Jahr im 20. Jahrhundert.
   - `19uu` kann ähnlich verwendet werden, um Unsicherheit auf einer bestimmten Stellenebene auszudrücken.
7. **Angaben von Jahren kleiner als -9999 und grösser 9999**
   - `Y-30000` für 30'000 Jahre vor unserer Zeitrechnung.

**Zusammengefasst**: EDTF bietet weit mehr Möglichkeiten als die Verwendung eines einfachen Kalenderdatums. Es erlaubt die Erfassung von Unsicherheiten, Unschärfen, komplexen Zeiträumen und offenen Enden, sowie die Angabe von Mengen, Intervallen oder wiederkehrenden Mustern. Das bedeutet im Kern: Wo man bislang nur ein genaues Datum hatte, lassen sich dank EDTF auch „ungefähr“, „nicht genau bekannt“, „innerhalb eines Jahrzehnts“, „irgendwann zwischen X und Y“ oder „eine von mehreren Möglichkeiten“ in einem einheitlichen, standardisierten Format darstellen. Diese Flexibilität macht EDTF für historische, bibliothekarische, archivische oder wissenschaftliche Projekte besonders nützlich.

## Datendokumentation

Die Stadt.Geschichte.Basel macht projektbezogene Daten in verschiedenen Formaten zugänglich. Verfügbar sind wissenschaftliche Publikationen mit Projektbezug einerseits, sowie die Metadaten zu den auf dieser Plattform bereitgestellten Quellen und historischen Forschungsdaten andererseits.

## Projektbezogene Publikationen

Die Arbeit des Teams für Forschungsdatenmanagement und Public History an dieser Plattform und weiteren Produkten wird ausführlich auf [dokumentation.stadtgeschichtebasel.ch](https://dokumentation.stadtgeschichtebasel.ch){:target="\_blank"} beschrieben. Dort werden neben projektbezogenen Publikationen auch Workflows, Guidelines und weitere Produkte zur Weiterverwendung präsentiert.

[![Screenshot der Dokumentationswebsite](assets/img/screenshots/dokumentation.png){:style="max-width: 50%; display: block; margin: auto;"}](https://dokumentation.stadtgeschichtebasel.ch){:target="\_blank"}

Wissenschaftliche Veröffentlichungen, die im Zusammenhang mit dem Forschungsprojekt stehen, sind auch [auf Zenodo archiviert](https://zenodo.org/communities/stadt-geschichte-basel){:target="\_blank"}. Die im Rahmen von Konferenzen und Workshops publizierten Beiträge des Teams für Forschungsdatenmanagement und Public History befassen sich mit der Entwicklung dieser Plattform und übergreifend mit (digitalem) Forschungsdatenmanagement und Public History in den Geschichtswissenschaften.
