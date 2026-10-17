# CommunityConnectNT

Emergency warnings, shelters and help for the Northern Territory — in the
languages people in Darwin actually speak.

> **This is a prototype, not an official emergency service.**
> In an emergency, follow AusAlert, the Bureau of Meteorology and
> [SecureNT](https://securent.nt.gov.au/). This app links to them; it never
> replaces them.

---

## Why this exists

Australia's new national warning system, **AusAlert**, went live in October
2026. It broadcasts a siren and a message to every phone near an emergency.
Its messages are in **English only**. The Emergency Management Minister has
said a siren can "move across language barriers" — true of the siren, not of
the message that follows it.

In Greater Darwin, about **one in three people speaks a language other than
English at home**, well above the national figure of roughly one in five. The
largest groups after English are Greek, Nepali, Tagalog, Mandarin and Filipino.
A further 10.4% of the population is Aboriginal or Torres Strait Islander, and
many Aboriginal Territorians speak English as a second or third language.

The Northern Territory Government's own emergency app, **secureNT**, was last
updated on **21 February 2017**. It is English only, iOS only, and has no live
warnings.

This gap has already caused harm. During Cyclone Trevor in March 2019, cyclone
information reached Ngukurr in English while the community speaks Kriol.
Residents could not tell how close the danger was. The Bureau had in fact
advised that Ngukurr would be relatively safe, but nobody there could read it,
so the panic continued. NT Emergency Services told the ABC at the time that it
had no policy on translating emergency messages into local languages.

A warning that cannot be understood is not a warning.

## What it does

- Shows current NT warnings with a **picture for the hazard**, so the kind of
  danger reads without any words at all.
- Explains the three Australian Warning System levels — Advice, Watch and Act,
  Emergency Warning — in the reader's own language, with the English kept in
  brackets, because English is the wording used on radio and TV.
- Lists nearby shelters with addresses and map links, and states clearly that
  you should not go to a shelter until authorities say it is open.
- Carries the emergency kit list and the phone numbers that matter.
- Shows the current Darwin weather and forecast.

### What it deliberately does not do

- **It is not the warning.** The Bureau, AusAlert and SecureNT are the
  authorities. This app always links out to them.
- **It never tells anyone what to do.** It does not say "evacuate" or "stay".
  It shows the official warning and explains what the levels mean.
- **It does not pretend to be current when it is not.** If the warnings feed
  stops updating for 30 minutes, the app removes every warning from the screen
  and sends the reader to an official source. Showing yesterday's cyclone
  warning as today's is the worst thing this app could do, so that failure is
  deliberately loud.

## Status

Working: 16 languages, hazard pictograms, warning-level explainer, shelter
list, emergency contacts, kit list, weather card, right-to-left layout for
Urdu and Arabic, light and dark themes, and the staleness guard.

Not finished, on purpose:

- **First Languages are listed but switched off.** Kriol, Yolŋu Matha,
  Pitjantjatjara, Warlpiri, Tiwi and Arrernte emergency wording must come from
  accredited interpreters and be checked with community representatives. The
  [NT Aboriginal Interpreter Service](https://nt.gov.au/community/interpreting-and-translating-services/aboriginal-interpreter-service/about-the-aboriginal-interpreting-service)
  is the right partner, and the Bureau already works with them during cyclones.
  Machine-translating an emergency instruction is not acceptable: "shelter in
  place" and "evacuate now" are opposite actions.
- **The shelter list is a snapshot** taken from the SecureNT website, which
  publishes it as plain HTML with no capacity figures and no data feed. A feed
  from the NT Government would fix this for every app in the Territory, not
  just this one.
- **The weather card still uses example data.**

## How it works

One HTML file, no build step, no framework, no tracking.

A scheduled job reads NT warning products from the Bureau of Meteorology's
anonymous FTP service every ten minutes, converts them to `warnings.json`, and
commits that file next to the app. The page fetches it from the same origin, so
there is no API key and no cross-origin request. If the file is missing, the
app shows clearly-labelled example data. If it is stale, the app hides the
warnings entirely.

| File | Purpose |
| --- | --- |
| `index.html` | The entire app |
| `fetch_warnings.py` | Reads the Bureau's FTP feed, writes `warnings.json` |
| `.github/workflows/warnings.yml` | Runs that script on a schedule |

## Run it yourself

```bash
python3 -m http.server 8000
```

Then open <http://localhost:8000>.

A web server is needed even locally. If you open `index.html` as a file,
the browser blocks it from fetching `warnings.json` and the app silently falls
back to example data.

To pull live warnings:

```bash
python3 fetch_warnings.py
```

## Data sources and credit

Warnings and weather come from the Australian Government **Bureau of
Meteorology**. Shelter information comes from **SecureNT**, Northern Territory
Government. Neither organisation endorses this app or is responsible for it.

Bureau data is used under its own terms, separately from the code licence.

## Licence

Code is MIT licensed — see [LICENSE](LICENSE). The licence covers the code
only, not the data.

---

Built by **Prakash Subedi**, Master of Information Technology,
Charles Darwin University, Darwin.

This project began as coursework for PRT551 Project Management, Risk and
Reliability, and is being developed toward a working release before the
2027–28 wet season.
