---
title: Datendokumentation
layout: page
permalink: /data.html
---

# Datendokumentation

## Projektbezogene Publikationen

Wissenschaftliche Veröffentlichungen, die im Zusammenhang mit dem Forschungsprojekt stehen, sind [auf Zenodo archiviert](https://zenodo.org/communities/stadt-geschichte-basel){:target="\_blank"}. Die im Rahmen von Konferenzen und Workshops publizierten Beiträge des Teams für Forschungsdatenmanagement und Public History befassen sich mit der Entwicklung dieser Plattform und übergreifend mit (digitalem) Forschungsdatenmanagement und Public History in den Geschichtswissenschaften.

## Datenarchiv

Die Stadt.Geschichte.Basel macht projektbezogene Daten in verschiedenen Formaten zugänglich. Verfügbar sind wissenschaftliche Publikationen mit Projektbezug einerseits, sowie die Metadaten zu den auf dieser Plattform bereitgestellten Quellen und historischen Forschungsdaten andererseits. Diese Metadaten sind auf der Grundlage des [Handbuchs zur Erstellung diskriminierungsfreier Metadaten für historische Quellen und Forschungsdaten](https://maehr.github.io/diskriminierungsfreie-metadaten/){:target="\_blank"} erstellt und aufbereitet worden.

## Datenmodell

Metadaten für die auf der Forschungsdatenplattform vorgestellten Elemente werden gemäss einem Datenmodell bereitgestellt, das vom Stadt.Geschichte.Basel Research Data Management Team entwickelt wurde, um den Anforderungen der vielfältigen im Projekt verwendeten Quellen gerecht zu werden. Das Datenmodell (und der anschliessende Annotationsprozess) folgen dem [Handbuch zur Erstellung diskriminerungsfreier Metadaten für historische Quellen und Forschungsdaten](https://maehr.github.io/diskriminierungsfreie-metadaten/), das von Stadt.Geschichte.Basel entwickelt wurde.

Die folgende Grafik veranschaulicht das Datenmodell mit Metadatenfeldern für ein Beispiel-Metadatenobjekt `sgb01313`, das ein untergeordnetes Medienobjekt `m01313` hat. Wenn ein Metadatenobjekt mehr als ein untergeordnetes Medienobjekt hat, werden die `id`-Nummern der untergeordneten Objekte fortlaufend nummeriert: `m01313_1`, `m01313_2` usw.
<img width="563" alt="Datenmodell" src="assets/img/sgb_datamodel.png">


## EDTF

Das [Extended Date Time Format (EDTF)](https://www.loc.gov/standards/datetime/) ist ein auf [ISO 8601 ](https://www.iso.org/iso-8601-date-and-time-format.html) aufbauender Standard, der über einfache Datumsangaben hinausgeht und es ermöglicht, komplexe, unsichere, ungefähre oder mehrdeutige Zeitangaben strukturiert und maschinenlesbar festzuhalten. Die wichtigsten Funktionalitäten und Merkmale sind:

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
    - Unvollständige Intervalle wie `1900/...` oder `.../1950` drücken offene Zeiträume aus („seit 1900“ oder „bis 1950“).
    
    Diese Intervalle können ebenfalls Unsicherheits- oder Ungefähr-Zeichen enthalten, um vage Zeiträume darzustellen: `1900~/1950?`.
    
4. **Listen und Sets von Daten**  
    Man kann mehrere mögliche oder relevante Daten in einer Liste angeben:
    
    - Listen: `[1960, 1962, 1965]` bedeutet eine explizite Aufzählung von möglichen oder relevanten Daten.

5. **Saisons und Quartale**  
    EDTF erlaubt die Angabe von Jahreszeiten oder Quartalen, die in manchen Zusammenhängen relevant sein können:
    
    - `1960-21` kann beispielsweise „Frühling 1960“ darstellen, wenn eine entsprechende Zuordnung der Jahreszeiten festgelegt wurde.
    - Der genaue Umgang mit Saisons ist festgelegt, um diese einheitlich anzugeben.
6. **Jahrhunderte, Jahrzehnte und unvollständige Angaben**  
    Statt eines konkreten Jahres kann man ganze Jahrzehnte oder Jahrhunderte angeben:
    
    - `19xx` für ein unbekanntes Jahr im 20. Jahrhundert.
    - `19xx?` für ein ungefähres oder unsicheres Jahr im 20. Jahrhundert.
    - `19uu` kann ähnlich verwendet werden, um Unsicherheit auf einer bestimmten Stellenebene auszudrücken.
7. **Angaben von Jahren kleiner als -9999 und grösser 9999**

   - `Y-30000` für 30'000 Jahre vor unserer Zeitrechnung.

**Zusammengefasst**: EDTF bietet weit mehr Möglichkeiten als ein einfaches Kalenderdatum. Es erlaubt die Erfassung von Unsicherheiten, Unschärfen, komplexen Zeiträumen und offenen Enden, sowie die Angabe von Mengen, Intervallen oder wiederkehrenden Mustern. Für Laien bedeutet das im Kern: Wo man bislang nur ein genaues Datum hatte, lassen sich jetzt auch „ungefähr“, „nicht genau bekannt“, „innerhalb eines Jahrzehnts“, „irgendwann zwischen X und Y“ oder „eine von mehreren Möglichkeiten“ in einem einheitlichen, standardisierten Format darstellen. Diese Flexibilität macht EDTF für historische, bibliothekarische, archivische oder wissenschaftliche Projekte besonders nützlich.
