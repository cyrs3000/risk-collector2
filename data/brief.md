# brief 2026-11-20T12:59:04Z

## sources
adsb:partial: 1 point(s) failed, firms:ok, markets:error: RuntimeError: all market symbols , iran_fx:ok, news:partial: 10 feed(s) failed: Times of Isr, telegram:ok, safeairspace:ok, polymarket:ok, state_dept:ok, embassy_alerts:error: RuntimeError: no embassy feed rea, fcdo:ok, easa_czib:ok, faa:ok, portwatch_hormuz:ok, marad:error: HTTPError: 403 Client Error: Forb, official_statements:ok, ofac:ok, ioda_iran:ok, gdelt:error: HTTPError: 429 Client Error: Too , usgs_seismic:ok, notams:error: RuntimeError: no NOTAM source rea, foreign_advisories:ok, ais_military:ok

## ALERTS (verify before use)
- {"type": "adsb_isr_above_baseline", "now": 3, "median_14d": 0, "p90_14d": 2}
- {"type": "foreign_advisory_changed", "src": "Switzerland Iran", "country": null, "level": null, "snippet": " Access Denied Access Denied You don't have permission to access \"http&#58;&#47;&#47;www&#46;eda&#46;admin&#46;ch&#47;eda&#47;en&#47;fdfa&#47;representations&#45;and&#45;travel&#45;advice&#47;iran&#47;travel&#45;advice&#45;iran&#46;html\" on this server. Reference&#32;&#35;18&#46;460ec617
- {"type": "foreign_advisory_changed", "src": "Netherlands Iran", "country": null, "level": null, "snippet": " Reisadvies Iran | Ministerie van Buitenlandse Zaken | NederlandWereldwijd Ga direct naar inhoud Naar de homepage van www.nederlandwereldwijd.nl Ministerie van Buitenlandse Zaken Menu Home Familie Geld Gezondheid Identiteit Onderwijs Reizen Vervoer Werk Wonen Onderwerpen A-Z Contact Zoeken
- {"type": "military_ship_ais", "mmsi": 209969000, "name": "IRIS", "ais_type": null, "dest": null, "lat": 32.81871, "lon": 35.01287, "area": "Eastern Med", "t": "2026-11-20 13:06:51.409111342 +0000 UTC", "first": "2026-11-17T22:56:27Z", "last": "2026-11-20T12:59:04Z"}

## military air (ADS-B, 24h)
points: Gulf 91/2mil; Israel 56/1mil; Saudi/Qatar 17/0mil; Iraq/Kuwait 7/0mil; Cyprus 76/2mil; Ramstein 726/18mil; UK 822/42mil; Crete 31/0mil; Incirlik 45/1mil; Tehran 0/0mil; Al Udeid 89/2mil; Prince Sultan AB 24/0mil; Muwaffaq Salti None/Nonemil; Diego Garcia 0/0mil; Akrotiri 77/3mil; Souda 31/0mil; Moron 215/3mil; Lajes 2/0mil; Mildenhall 803/42mil; Red Sea 0/0mil; Arabian Sea 0/0mil; Caspian/Baku 4/0mil; Ashgabat 0/0mil; Yerevan/Nakhchivan 22/0mil; Van/Tabriz rim 16/0mil; Iraq-Iran border 1/0mil; Basra/Khuzestan rim 21/0mil; UAE/Bandar Abbas rim 102/2mil; Muscat/Oman 79/2mil; Herat/Mashhad rim 0/0mil
baseline: tanker now 4 med 1; transport now 7 med 2; bomber now 0 med 0; isr now 3 med 0; gov now 0 med 0; bridge_ir now 4 med 1; mil now 66 med 9
- 13:18-13:18Z NATO04 E3TF (isr) Moron
- 12:59-12:59Z RRR7220 R135 (isr) Ramstein
- 12:59-12:59Z NATO03 E3TF (isr) Ramstein
- 12:59-12:59Z IAM1491 GLF5 (isr) Ramstein
- 13:18-13:18Z ? K35R (tanker) Gulf
- 13:18-13:18Z VADER39 A332 (tanker) Israel
- 13:18-13:18Z MMF21 A332 (tanker) Ramstein
- 13:18-13:18Z ? K35R (tanker) Ramstein
- 13:18-13:18Z RRR2120 A332 (tanker) Ramstein
- 13:18-13:18Z ? K35R (tanker) UK
- 13:18-13:18Z ? B762 (tanker) UAE/Bandar Abbas rim
- 13:18-13:18Z FAF4097 A332 (tanker) global:mil
- 12:59-12:59Z ? B762 (tanker) Gulf
- 12:59-12:59Z ? K35R (tanker) UK
- 12:59-12:59Z ? K35R (tanker) UK
- 12:59-12:59Z ? K35R (tanker) UK
- 14:30-13:18Z CNTOR30 A400 (transport) UK
- 22:56-13:18Z JIGSW93 A400 (transport) UK
- 04:27-13:18Z RCH2002 C17 (transport) Cyprus,Ramstein,global:mil
- 13:18-12:59Z RJAF363 IL76 (transport) Cyprus,Israel
- 13:18-13:18Z BLADE38 A400 (transport) Ramstein
- 13:18-13:18Z CTM0030 A400 (transport) Ramstein
- 13:18-13:18Z RCH8051 C17 (transport) Ramstein
- 13:18-13:18Z RCH2195 C5M (transport) Ramstein
- 13:18-13:18Z BAF666 A400 (transport) Ramstein
- 13:18-13:18Z BNDGE01 C17 (transport) UK
- 13:18-13:18Z GAF310 C30J (transport) UK
- 13:18-13:18Z BCAT841 C17 (transport) UK
- 12:59-12:59Z CNV6519 C130 (transport) Ramstein
- 12:59-12:59Z RCH5092 C17 (transport) Ramstein
- 12:59-12:59Z GAF316 C30J (transport) Ramstein
- 12:59-12:59Z RRR6629 C17 (transport) Akrotiri
- 12:59-12:59Z GAF142 A400 (transport) Moron
- 12:59-12:59Z UAF1250 C17 (transport) UAE/Bandar Abbas rim

## Iran airbridge & state flights (24h; IR/RU/CN/BY regs, heavy cargo types, sanctioned callsigns) — 10
global: {"mil": 7, "type/IL76": 1, "type/A124": "error: ADS-B sources failed: api.airplanes.live HTTPError", "type/Y20": "error: ADS-B sources failed: api.airplanes.live HTTPError", "type/IL62": 0, "type/IL96": 0}
- 12:59Z ? B735 EP-FSQ [IR] Iranian-registered @27.500381,54.345375 alt 23275 trk None Gulf
- 12:59Z BRU717 A332 EW-589PD [BY] BY-registered in region @25.258418,55.34951 alt ground trk None Al Udeid
- 12:59Z FIE3533   [] Iran-linked/sanctioned cargo or RU/BY/CN state callsign @40.76072,40.056652 alt 36000 trk 281.87 Yerevan/Nakhchivan
- 12:59Z FIE3583 B735 EK73736 [] Iran-linked/sanctioned cargo or RU/BY/CN state callsign @40.150549,44.403383 alt ground trk None Yerevan/Nakhchivan
- 22:11Z AZS4103 IL76 RA-76834 [RU] Iran-linked/sanctioned cargo or RU/BY/CN state callsign @23.957748,58.98819 alt 27575 trk 42.5 UAE/Bandar Abbas rim
- 22:11Z BRU8196 B738 EW-544PA [BY] BY-registered in region @32.39241,37.59527 alt 32000 trk 39.08 Israel
- 22:11Z FIE3633 A320 ER-00016 [] Iran-linked/sanctioned cargo or RU/BY/CN state callsign @29.209488,48.879653 alt 34975 trk 153.23 Basra/Khuzestan rim
- 13:18Z RSB7684 IL76 EW-567TH [BY] heavy military/state cargo type IL76 (BY) @None,None alt 36000 trk 356.66 global:type/IL76
- 13:18Z VDA8267 A124 RA-82074 [RU] Iran-linked/sanctioned cargo or RU/BY/CN state callsign @None,None alt ground trk None Gulf
- 13:18Z FIE3349 A320 EK-FOG [] Iran-linked/sanctioned cargo or RU/BY/CN state callsign @40.150514,44.403383 alt ground trk None Van/Tabriz rim

## government/VIP flights (24h) — 3
- 22:11Z BAFCO 81    @26.264305,50.6378 trk None Gulf
- 13:18Z BAFCO 86    @26.262957,50.638376 trk 140.62 Gulf
- 13:18Z SAMU59 EC45 F-HNOR  @50.476452,3.257892 trk 131.74 Ramstein

## FIRMS: total 497, not oil/gas 112 (median 62.5)
- near [('Bandar Abbas', 16)] frp 7.89 2026-11-20 34
- near [('Bandar Abbas', 17)] frp 2.76 2026-11-20 956
- near [('Kermanshah', 20)] frp 2.24 2026-11-20 958

## markets: 
iran fx: {"usd_rial": 2699700, "usd_toman": 269970, "emami_coin_rial": 2495900000, "emami_coin_toman": 249590000, "gold18_rial": 242867000, "gold18_toman": 24286700}

## official
- Hormuz transits {'date': '2026-11-15', 'total': 2, 'tanker': 0, 'cargo': 2} median 3
- StateDept: Iran - Level 4: Do Not Travel
- StateDept: Syria - Level 4: Do Not Travel
- StateDept: Yemen - Level 4: Do Not Travel
- StateDept: Bahrain - Level 3: Reconsider Travel
- StateDept: Jordan - Level 3: Reconsider Travel
- StateDept: Lebanon - Level 4: Do Not Travel
- StateDept: Oman - Level 3: Reconsider Travel
- StateDept: Saudi Arabia - Level 3: Reconsider Travel
- StateDept: Kuwait - Level 3: Reconsider Travel
- StateDept: Iraq - Level 4: Do Not Travel
- StateDept: United Arab Emirates - Level 3: Reconsider Travel
- StateDept: Qatar - Level 3: Reconsider Travel
- StateDept: Israel - Level 3: Reconsider Travel
- StateDept: Pakistan - Level 3: Reconsider Travel
- StateDept: Turkey - Level 2: Exercise Increased Caution
- StateDept: Cyprus - Level 1: Exercise Normal Precautions
- StateDept: Afghanistan - Level 4: Do Not Travel
- StateDept: Romania - Level 1: Exercise Normal Precautions
- StateDept: Egypt - Level 2: Exercise Increased Caution
- IODA Iran: {"events_48h": [], "bgp_latest": 41762, "bgp_median_48h": 41763, "bgp_drop_pct": 0.0}
- GDELT: null
- Advisory {"src": "Germany", "country": "Iran", "level": "warning", "modified": "2026-10-29T14:28:09Z", "changed_since_last_check": false}
- Advisory {"src": "Switzerland Iran", "changed_since_last_check": true, "snippet": " Access Denied Access Denied You don't have permission to access \"http&#58;&#47;&#47;www&#46;eda&#46;admin&#46;ch&#47;eda&#47;en&#47;fdfa&#47;representations&#45;and&#45;travel&#45;advi
- Advisory {"src": "Netherlands Iran", "changed_since_last_check": true, "snippet": " Reisadvies Iran | Ministerie van Buitenlandse Zaken | NederlandWereldwijd Ga direct naar inhoud Naar de homepage van www.nederlandwereldwijd.nl Ministerie van Buitenlandse Zaken Menu Ho
- AIS mil IRIS (209969000) Eastern Med last 2026-11-20T12:59:04Z
- civil traffic vs same hour: 

## polymarket
- Israel x Iran ceasefire continues through November 22?: {'Yes': '0.89', 'No': '0.11'}
- Israel x Iran ceasefire continues through November 20?: {'Yes': '0.9845', 'No': '0.0155'}
- Israel x Iran ceasefire continues through November 30?: {'Yes': '0.825', 'No': '0.175'}
- Iran leadership change by November 30?: {'Yes': '0.0135', 'No': '0.9865'}
- Will the U.S. invade Iran before 2027?: {'Yes': '0.065', 'No': '0.935'}
- Israel x Iran ceasefire continues through December 31?: {'Yes': '0.625', 'No': '0.375'}
- Will Benjamin Netanyahu be the next Prime Minister of Israel?: {'Yes': '0.208', 'No': '0.792'}
- US-Iran Final Nuclear Deal by November 30, 2026?: {'Yes': '0.0065', 'No': '0.9935'}
- Strait of Hormuz traffic returns to normal by December 31?: {'Yes': '0.0315', 'No': '0.9685'}
- Iran full airspace closure by November 30, 2026?: {'Yes': '0.075', 'No': '0.925'}

## news (multi-source first; outlets count)
- [23] Iran widens Gulf attacks by targeting a US air base in Kuwait and sites in Bahrain | AP News, CoastTV, Toronto Star, Herald Bulletin | https://news.google.com/rss/articles/CBMimwFBVV95cUxQVkpMQk5Ha1FZNG45Vmt6WWxWeUtMS3lSU0hON0F0b0ItSHlWY0NnUHFyQ1JTWFBPSWViZTFVZHpKNWI3V3R1TjM0b25HWTNEZGZ2Q1ItZG5hdXNGcG03M3FjZlJKNmE5SC1lYTJERmRETERvdGJOUGlsMG9pQjVVU2dEWkJxOEY2eXJYd1RtVmNlN2pIcGlLcHJlaw?oc=5
- [7] Iranian Army: Three Tankers Catch Fire After Hitting Naval Mines in Eastern Strait of Hormuz | WANA News Agency, Al Arabiya English, marketscreener.com, Cyprus Mail | https://news.google.com/rss/articles/CBMisAFBVV95cUxQVG90ZEVCTHlyUXBhZVlOSGRLX2hKeFIwNWNmc2I5U2M1SnJJQ1F0U094RW1lUzg2ZlIyUWR4dHlnSnNleUxZN3RnX2dqOUhLQ1VBVEVTNndhSEgtVGV5ZHh0bWpkWTFsQ21tVC04S1RNM1JEZFQ5eVpxZDBEN2RsWFVzTmVZd1J4Zl9Ec2NERkplWmR0RDJtNjlrZm5yZlJrWlVBa1RzS0V6UHdpU25nUA?oc=5
- [4] Mossad chief called for renewed strikes on Iran during Washington visit | Nacionale, The Times of Israel, WSJ, The Australian | https://news.google.com/rss/articles/CBMioAFBVV95cUxQamxHcEh3WEh1eGNGUkhkTmlsWEp6MXljUVZnQWNvcjdpQ1Z5U0JFS1dyQlAtX3JITjJoN1c3SkdXOEZDeE9TbjBfaVhQSk45dEFiLVVZN200T1gyX0dHRVhaM1dsa3k1NHhkYzFKaXBuNDhZR1llZ2pWX3dKWmlXcG43UmpLcnFNcE1LR0oyU2NmcFpfa3loRXUwanljdXVW?oc=5
- [3] Trump says he won’t ask Xi or Putin for help on Iran | Iran International, TV7 Israel News, Foundation for Defense of Democracies | https://www.iranintl.com/en/202611199940
- [3] Moscow, Beijing, Tehran say UN nuclear watchdog can resume inspections in Iran after hostilities end | Anadolu Ajansı, The Nation (Pakistan ), NewsCord | https://news.google.com/rss/articles/CBMi1AFBVV95cUxQcGZRcm8zMjJnQ1Zfcng3QU5KbTV6ZzIwMFdVRy1mQTZ5b2c5YU5ibENiTzU1ZDF0aVBQQVE3Q2UwVkxlVHNlNFFTc0s2U09ka2psUXNwclVGTVJ5WXg2eU9yU3dhSG9BQ2g1S0R4bEVwZDF5blk1S0dlbHdtZ2hxWGZDWDdoT1ZlWUxpMXpxdmZvQVVsU1hFQ2ZSQjZfNm0wWGJoYXVTSkZQVW9LdFU0bE1GZ011TWhnRXhpczJ1Uk1FelpzNnlSbnA4MFhsRFk0V3lPWQ?oc=5
- [3] Iran Intensifies Hormuz Tanker Attacks Just as Oil Prices Slide | gCaptain, Bloomberg.com, Crude Oil Prices Today | OilPrice.com | https://gcaptain.com/iran-intensifies-hormuz-tanker-attacks-just-as-oil-prices-slide/
- [3] Factbox-Houthi attacks on Saudi Arabia | Internazionale, سانا, EA WorldView | https://news.google.com/rss/articles/CBMipAFBVV95cUxNTllxSWJLNjZBaEU1TU9tOWNZV1dFeDEtWVA4MGhnajN1Y0M2LXRLMnRCTjctWmRSVWZ4cHIyZ3JUbEJXdElHeFRVa1hXT1hTNk9IbS1NV0xveHdZcVp5cFhFMnJfMVY0QnB4S080cjMzSDFfMWZuMTJfNkZmd0tybmhrN1F5anltM21ENHNZWHFBMjNrWE5fSkFzUUEtX3RNSnlxQQ?oc=5
- [2] Israeli ambassador: US troops will come home from Middle East ‘when Iran is defeated’ | The Times of Israel, The Jerusalem Post | https://news.google.com/rss/articles/CBMixwFBVV95cUxOTXFBaXBsMElvY2FvTEVFeTRhdjNCSmxmQmpaYXVXaDlNcDdEdXVZM0xENmloWHVWZTVmY1NTYTFaYkJfeU1VdTZhenMxeF9laEJDXy10NmwwYU1PZ21vUnBwRDREbG5NeGFCYm5YYkxSSEVVcElfODNHaXF3RFRkSG9BOFY2TW9kUExrcFNhV2x2WEM1aDU0dE5HdDNHZzVZZ2xRT3hxYWpzQXJxVG5kWlg5MjFwVk5abUQ4RmVRbjlSdDNTbWlj?oc=5
- [2] Top US General Huddles With Israel As Iran War Clouds Gather | AOL.com, BizPac Review | https://news.google.com/rss/articles/CBMifkFVX3lxTE9RZGVWd2tUcm5nS1ZXcVN3YU5XWXYzSnpQeGFFN091aGZQU3Nua3hyTnQ4UGN5ZTZnNU5kSXJzZU9scU9zYkZpS3JUVGMzOFVZLS1ZNVVOMzU3STV3VXdINF9oa3BBQjFYVnRSaW5jYTVENjhuU0U0TVc4Sko5dw?oc=5
- [2] "Holy S-, that’s Tehran": B-2 pilots reveal dramatic moments of strikes on nuclear sites | Israel National News, The Jerusalem Post | https://news.google.com/rss/articles/CBMiWkFVX3lxTFBKX01iRnpNOFhid1hTbFZsb2VfY2YzbXNQNXNfZDE1RkwxdG1GU1A5clFVeW9iWWdSN2RIOUdhbncybnZDY1dRNmdoOFRkZ1EwNFlMcEdGQjBEQQ?oc=5
- [2] Oil Tanker Catches Fire in Eastern Strait of Hormuz | WANA News Agency, تسنیم | https://news.google.com/rss/articles/CBMifkFVX3lxTE9yZ2psZzhaS1ZMOFpEaHAzeW9OWFJmWXhyS2J1aUllQ2R1b1ZMcERMUFpDSjJRSFM3aU9JSGxjaWRBcWVZbWRIUVBJREFZUThDN1VEQ1dzZnd0WjV6UGtDTnBublRIWWZtUEk4NTNRSTNxaGFVVEVFcGtZUEhwZw?oc=5
- [2] Iran rejects unlimited IAEA inspections amid continued military threats | خبرگزاری بین المللی قدس, Mehr News Agency | https://news.google.com/rss/articles/CBMiQkFVX3lxTE8wdWdHa3RFS0pEQl9ZV0N0dEM0V2JmbVl4MnJFUXpHeGlQOXlpbnU2VFVqQU5taG45UnQxUGlTZy16QQ?oc=5
- [2] Iran Links Nuclear Inspections to End of U.S. Military Threats | teleSUR English, Crude Oil Prices Today | OilPrice.com | https://news.google.com/rss/articles/CBMie0FVX3lxTE8xSEE2U19XcHJjQ1pSNWVJSlN0aFRkR3luQ1JuZkd4NnQ4MDZ1SFRKYmM5NEdXanA4WWpWaXBQT0pmTFlFbnV6ekVCODBwNk81d3I2T2FjeGpqZ3dVMWZ6RVVDTzhqUkFRMFd6NEZ6NVpoLTBObHFsSVNwRQ?oc=5
- [2] Israel upgrades David's Sling to counter wider range of Iranian missile threats | CTech, NewsCord | https://news.google.com/rss/articles/CBMiZ0FVX3lxTE9ob3FHa0p5MnZCRnB0b3BGcGhzZVJKUFRHN1lNWVYwb2VsTXlMRzUtTE1lZUlQVWdNR0RSelpLQUFUVEJPV0JPY19ScE4tTFhOWHlSYkRIVUlMeWN0WXJXQmR3ZFluVVE?oc=5
- [2] IRGC Chief Says Iran Controls Waters 500 km Beyond Strait of Hormuz | https://houseofsaud.com/, The New Region | https://news.google.com/rss/articles/CBMiggFBVV95cUxNZUZkUHpxZlFfSm9YbjZmNFVPZ0VSeGdoWnR4Y29VeXVIbV9vdDBXX2pGbENhZmQ2R3c2RThONERLaTNpaU5FOGd1RzBvLUJFVzRmbTNvU0ZQNlhLbVZENzdkOHpxNl9yUjE5bU9hUG1ldl9VOTVkVWxWSEtBM19XS213?oc=5
- [2] US tightens Iran blockade with curbs on ship-to-ship transfers | Shipping Telegraph, Homeland Security Today | https://news.google.com/rss/articles/CBMirwFBVV95cUxPVmt3a0NDNlJjTHNhcnBfeGpqWVVlSF8xa2p1bU5SMjJLQ0ZJOGdTd041MkJ1azQ3SW03d0lFMmVQX2dkQXJuemRUcTQ2ZDYwTnI4ZjhJYUNfUUtadUtHOHZBSHp0ZGV1bTNnd1JpcXJzTHdvcDM3bXcxcDR5MVo1aGxyQ1BiR1ZyblhTQkN4M3hMTG11LVlqdEFaNWQ2eG01Wi1paHYtX0NBVmNmeEJ3?oc=5
- [2] U.S. and European Powers Demand IAEA Access to Iran’s Bombed Nuclear Sites | IranWire, الحرة | https://news.google.com/rss/articles/CBMirAFBVV95cUxPZ3IzVEFwd2ZHRVRPZ0NyZmhJMW9RWDd1dmdRbU5PcVNYSWxQWXJCV182VEJCYVBTVW5DeGxiNUFMQV9EdElIcUZhdlB0SHVvaWNxT2MtN2Z6TWdwQ0V0LTd5ZWdkdGVXYW11a3lFN2lETE5IOTRUNHA1b25TN2Y1UlB2UldUQlJvckQ2RnFTcVZ2OWlYbVdQcXRDcW9NemVjd09oY2lzMWVEM04y?oc=5
- [1] US/Israel-Iran war: What UAE residents need to know today (Nov. 19, 2026) | Gulf News | https://news.google.com/rss/articles/CBMipwFBVV95cUxOcjZVeURGd1VYMjF2Mk1JWFNkajZjVHdzbFBPNkprTGd4anJWOFE4b1ZtaHRMZml3alMxWk43MFV0b3owRmFjUzJzcFRhV29VMk9NdHZOVU45WTNtSjZUOElfT1BqQXhrYU9lb1c4aTU1R3B1V2xLSGlZU21ZSVBtc3NyYTBhdXdQQl9ZLVIyTXlkR3NqamFGQjdUTlVTYlpsYzBWaDljY9IBtwFBVV95cUxPWDZ4Q093Ui05dDlLVVJoV2dPcVpzcXRFWlpZTUx5WDQxY0tlLXlUNXhLSy1LVWRfcEdlMzVhM1otZzNVM2dRc0lhQkdiMF9HYVg0TDZrLUN5X1B4SE8tSkYzWGpDa1hRV1VFWjhrNDdnQzZTaGROb2pURHhBT2JiY2pNWVpwRXdtTFl1bXQ1eXpHN25kcjZ5UzVIc3JoRWI4VnJKTUZxd1M5UGpsTjdlNEhfbjZZOHc?oc=5
- [1] Iran, China threats highlight need for Israel, Australia to rethink defense, experts warn | The Jerusalem Post | https://news.google.com/rss/articles/CBMiXEFVX3lxTE1acnhqYWZHY1lEQ3FFd19kYXUwd29nQ3h6OHZ1REFvZm04UE92R1BLUko5QmpNLW5tVkhsQzJ4NVFFN3lxOTRta0F5NmFRLVV1Z1haNUcxXzlyUHpG?oc=5
- [1] عربستان تایید کرد که بلندترین برج ریاض در حمله حوثی‌ها آسیب دیده است | BBC Persian | https://www.bbc.co.uk/persian/live/c6lyw484yd70t?at_medium=RSS&at_campaign=rss
- [1] Iran rules out unrestricted IAEA access under threat of renewed US-Israeli strikes | thecradle.co | https://news.google.com/rss/articles/CBMiT0FVX3lxTE9FTTJhTnRyM3ZCTDhIU1NQQ1oxRC1URk5QdldVS2JFbUQ1cDNnWlZVYUxfMXN0QnVvWUw5cWhmRVhpbENYY1hQTjFxZlcwV1k?oc=5
- [1] Strait of Hormuz Watch: Peace Negotiations Stall, Vessel Attacks Persist | IndustryWeek | https://news.google.com/rss/articles/CBMi1wFBVV95cUxQMzdGVkRCRkxtektNWVpJYUlyU2dMRFBSeVNxOVNsaHlDblpiblVTQ2d1SWotMmhUSk52YlNoalZKaGJkV1N4LUdjbXFFLVN4dk9JX1dYYnhZbHU1anY4QjBMNFF4N1JpVHNHNGUxcjk0YzRfSHFjWExic3NLTFFiVUhRVVhZaW1iZEt4eldXVFBfMnlaSmw0T1BMMnhfOGM2WmpROTF0OTZuc2t1Z1llRklEaVRwQ3FPT0tPdGo4Z052c3ZvQTMyVnRrVk9xM1JKRGJsUjhVMA?oc=5
- [1] Natural Gas, WTI Oil, Brent Oil Forecasts – Oil Rebounds As Iran Intensifies Attacks In Hormuz | FXEmpire | https://news.google.com/rss/articles/CBMi2AFBVV95cUxQdENuTHpJRmszRU11b1E3VlVfNDJ3QkhtYVk1RjBjV2d2X1Rpa2x0VjM1c2J3YzR2VklEdGlhbjhockMzZ1VZZ0VENV84M1haTnN1MUJZQ2xmS1ZtcWczSnVwbU9OZlRuVExVSjdfTkRncTF5TlBYcTI2Zzk5RDdpLVpvRXpqQ19oRFpXWUZkd2lYRG9pb00wRGlNSG9Ud2dXckVvWlFsWWVzc0xxamNQMll3UnhLMHc3N3ZXVHdkUE9PaEhLQ29nZFRISF9ERXdXVDdMalZPSXo?oc=5
- [1] West Demands Iran Restore Access to Bombed Nuclear Sites | tovima.com | https://news.google.com/rss/articles/CBMijwFBVV95cUxNNXNfcTZCbGhNeXk4TWtDN2tMRWpfcTlzR1pmM2o3QUtmQmI0R05idWU4VGZKbVg3a0tVZE14c1pxT2hCYS1iRDFCbzlWeEQzZDFmSG90V1JDZmgxOGJabmw2UEFVcjVSSU5IYklCSmpueTZXZDBGbGdvdnFPb0Z0MUc5UkcxdWc1VW8tSEtxSQ?oc=5
- [1] US targets Iran’s ship-to-ship transfers: Can Tehran break the blockade? | Al Jazeera | https://www.aljazeera.com/news/2026/11/20/us-targets-irans-ship-to-ship-transfers-can-tehran-break-the-blockade?traffic_source=rss
- [1] Kataib Hezbollah faces deadline to leave Iraqi stronghold | Al Jazeera | https://www.aljazeera.com/video/newsfeed/2026/11/20/kataib-hezbollah-faces-deadline-to-leave-iraqi-stronghold?traffic_source=rss
- [1] Drone operator removes Man United training footage and issues apology | Al Jazeera | https://www.aljazeera.com/sports/2026/11/20/drone-operator-removes-man-united-training-footage-and-issues-apology?traffic_source=rss
- [1] ورود نیروهای دولتی عراق به پایگاه کتائب حزب‌الله، از گروه‌های مورد حمایت ایران، در جرف‌نصر | BBC Persian | https://www.bbc.co.uk/persian/live/cmqx50ez02ent?at_medium=RSS&at_campaign=rss
- [1] در واشنگتن چه می‌گذرد؟ اختلاف بر سر ادامه جنگ با ایران | BBC Persian | https://www.bbc.com/persian/articles/cqe85mn3k0n1o?at_medium=RSS&at_campaign=rss
- [1] چرا گزارش نیویورک‌تایمز درباره سدهای ایران جنجالی شد؟ | BBC Persian | https://www.bbc.com/persian/articles/cmd71ee82dx0o?at_medium=RSS&at_campaign=rss
- [1] Ex-boyfriend shoots woman dead at her birthday party in Iran | Iran International | https://www.iranintl.com/en/202611207521
- [1] Iran sentences taekwondo champion to death over January protests | Iran International | https://www.iranintl.com/en/202611200129
- [1] Iraq begins taking back town held for a decade by Iran’s strongest militia ally | Iran International | https://www.iranintl.com/en/202611200850
- [1] Ideology or history? Analysts clash over the roots of Iran’s enmity with the US | Iran International | https://www.iranintl.com/en/202611198764
- [1] UK running offensive cyber operations against Iran, Russia and China - Sky News | Iran International | https://www.iranintl.com/en/202611206064
- [1] Iraq reaches deal with Iran-backed militia over Baghdad stronghold | Iran International | https://www.iranintl.com/en/202611205946
- [1] IRGC says Iran International is among its military targets | Iran International | https://www.iranintl.com/en/202611201108
- [1] U.S. and Israel considering new assault on Iran, sources say | CBS News | https://news.google.com/rss/articles/CBMijAFBVV95cUxOdzFPc1pJbDNCSGFPdEUxQjJ6ZTl0eGc2RlYwNVZ0WS1GRnVUWGNtemhtNENVcGFReklwbU9uSVFJcnBRSFJqTFVTX0hqc2VHSG16cUpiY2pCSW5JQ2hWa1J6RzZ2NENMQjQ2LTJNd3A5VFNWNGtFckRpaUFxdzlxN3JfVldfRmVmWE5SVg?oc=5
- [1] ‘We’ve Got Time’: Trump Suggests Iran War Will Continue Into 2027 | Time Magazine | https://news.google.com/rss/articles/CBMikAFBVV95cUxOQjZGUzREbXRjRmtjM2dNZXc5eXVvVEJJOUdFdkpRNnZXVngwcDItZE9JYnJQc0diN3dRU1p3OGMzY0RQRkw4Q244ckR3UWVFWVc3ZkJHeThzU09aWnE4SHhxcVJqdld4bUtrdmdaVjA0QUdWT3dySkwzc0VVZXRDcWlHaTBZNERRWTUxbG1ZMzk?oc=5
- [1] Israel Pivots to Cheaper Air Defense With Iran Tensions Rising | Bloomberg.com | https://news.google.com/rss/articles/CBMizgFBVV95cUxPeU84OXZxbno1dGNIaFh0YjI0SDN0dk94TmtDTmJRNjhzbUp1bXNEcHoyMUxnMjZjUFpLQXJqR1YxbmFyb1djNXJBaVROV2kybWxNT1pHT0RGMVJINXl0VkpJajdzWUE5QUdFTTVxWWtyZF9obm9qSXhmY29VQTVSZXpqRGpFWXNyNFp2RDJKUjNCLWFQajNKSURBTkxRM29tZVdlMHpGaEJwbGJudUtDTWV4dTk0UmJ1Z3ZOWG5XZFdfcE54RzJaWVJfdnlzZw?oc=5
- [1] Opinion | Israel must prepare for more war on Iran, but not every threat justifies it | Haaretz | https://news.google.com/rss/articles/CBMijwJBVV95cUxPVXlKc1JSRnFlU2xaTWFxT3hueG5BRzliTkdKbnpaRTRKcG1yUnRwblhJM05teVhGNEJhODgxQ2Q4WFZ3X21ibzlDNlZBQ2MtUU1RR1pyM2lVSll0RlRRSXYzeG1JUHFaZXpFSW9MdkQ1clRjaFdFa0JJZkNtTVJpZ3JHRlVxMGVtLVp3bEFoZnZDenZGbk1YOW1YcEVWa1NMRFg2ZHhaX1lJVWM0X19pM2t1T0I2azB6ems3am54c2c3NHlxTm85T0VMbmlUUjl0RTlPWUF2ZURLY2pwWGUzcFhKSzBGbHNQSmJaazFSSHdGZllydUUyWEVLaG9VNXJuYm1Hcm40V3JNVFJoa3BJ?oc=5
- [1] President Trump is weighing plans for another round of extensive military strikes on Iran amid intensifying pressure from Israel, according to U.S. and Israeli officials. | Facebook | https://news.google.com/rss/articles/CBMi0wFBVV95cUxOTTMzRVpVZmViaENjSHVTVW82Q0F3U3YtbHZZOWdsVlJQQXpHbjgwT2tIeWJfaHJka1IxQkgta09waUdyaVpsa0xhbFVuUHo1ZGhhUGk3LUFQbXlGVVVLX29tZ0xSaHZ0bnBKNXAtRFBCcTJ5empsTTc3R2RTNlZ6cWN1RXRJVnE1MjlBeFVSU2FsX0NpbXFBU1BYT2tLLUlOaVNmMzRQNlhxMzk2YXdVSl9VaGg0NktRY2xlSUNpSGZkV3JINVJQS29QM3FBRjlhd3Zn?oc=5
- [1] Israel, US could launch joint strike on Iran within weeks, ex-Navy chief says | The Jerusalem Post | https://news.google.com/rss/articles/CBMiakFVX3lxTE9VaDR3cGtCckhHamdYMG0yYlFYamFadlp1MEFMUlBSbmpJb1RWdjVDMzUteWVnWlYyVE9KRV9pQzJiMTdnNGNONS0yTzFMN3VlYTQ1eWhyTGxmS0dyOXYxOVJnbzBSZ202X2c?oc=5
- [1] Trump says Tehran may be working on chemical or biological weapons as tension mounts | CBS News | https://news.google.com/rss/articles/CBMilgFBVV95cUxNczRzemtDSHlJLXZIOHl1WHVMYUZkLTFMd1Z4TDJHNWhDa2E3djdWWnM4MXlwbXpnYjNyUU9TcXR6YjhsOWRVS29ub25Dd0pLVWNZRFZWR25CdnNxeTQ4VDRYX2g1dlFqZmQ1N1o1WWowQk5XRTJvSnhwWENzaXlBSF83RW5kbE5FelFKa0J2dnlhQVJJTkE?oc=5
- [1] As Trump Weighs Iran Decision, Israel Faces Growing Pressure from Young Evangelicals, El-Sayed | CBN.com | https://news.google.com/rss/articles/CBMisgFBVV95cUxPY1daZFJvaFZjNG0wczExRFpKUGE5eml1T2JrLUxkZEZnYzdGdFI2M0JreXFycWR5QW9mRnJwMVFXT1Izbi1nVGdGT05tRnE2bUVibHpNMkRQQzhoTnUzZkpoancxek55ZGNXenBFUFFsdmtRRjN2QngyUTY4YktSVjNzRkZzeV83bV8yUFpFZ1dudjVialFVS0VyUUxxUGZJNUwyTXpleVNGVVlXV2I3N1dR?oc=5
- [1] Israel May Act Against Iran Without Trump, as Regime Change Is Seen as the Only Lasting Solution: Top Dip | Benzinga | https://news.google.com/rss/articles/CBMilAJBVV95cUxOMWFLUnNtSzkyYmNsNWM5emdfSmlxaE5vTnhySmltbTJxOTJDOUtyOE1sMlRhamdCYnJWOW90RjZhSzh0ZzVhQWc4VGpoWlFFdVNBWGtCcjJsUUN5Z1llX1VMZ3NCZmdyQ2h3NXZFZVhTU3JzTXk1R3dEcjdmMFdHU3BGZ2VlQ1Y0SktQRW16QkR1SWVvM044T293M28wYmxidXR3Um0tXzMwcEFFUVhjOUk2aVdKTVpuejdKbERJTThYZ2ZCX2E3dlRubERGcmY0LXVpSWhrdVQ4dkJLU1I3T3lJZ08yMFg2dThqQ0hCVEZKczlpUkViR19JVTZ0VVFDV0hJUHMyekZVRVl4bmY1bmlOWkI?oc=5
- [1] IRGC Chief Says Iran Ready for Continued Confrontation with US and Israel | WANA News Agency | https://news.google.com/rss/articles/CBMimAFBVV95cUxQc2FETTBkZlN3d2NDWlBDbDNSTXl2SlMzcHFHdjc5VlpOSk9jRTdqcXNyRHhVMDFFUFNKVEF2NjhVRFZWMUtQSDZmbWl3c1l6TC1GcmhBVXdKMUpDeFdaay1wakZUcFctWUpPMWp1a0ptdHIyNWM5UlNNcVFfeDVocEdkdy01YU5wS0JCQjZnQXNmRy1RWVV2MQ?oc=5
- [1] US maritime agency warned Iran blockade was adding to rising Gulf premiums | Al Jazeera | https://news.google.com/rss/articles/CBMiuwFBVV95cUxNOWRhVjVJU0FZNUcyXzNUMkx2YnZRZ09iSFIwZGxpSEppeE5sb2M3SnVHanFhX2lsRUFmUERUbWU3OTgyM01MWXptNmZ1WEVBUUpsZlJEdmdpZGwyQVFiLTRHcVZGSW5weFMySmxHZFZCcFl2WTkzenJxSUtwd1Fta3NJSFBhQXFhd0xqVmV2Z0daS3NIS3R4Y1gwYXBxQVJqZnNKakJHLWRvdmdJZnBJeXJjLUtPRUh2WGtN0gHAAUFVX3lxTE5ERFVNRUhmckVtM1NQelV0YVFwV05xRmZQbzVDd1ZyUHF3cEVOUG1FSEhEaTBURVlXS2lhcnFreXFZajQ5VXN2QUpsbGVqOFhPVS04U2hPNGlwZ0MwVG5RNG8tZTZEVGdZcGVGbTZzLU1JSTVMUGlUVVZBRW8wRXZjMVJJa0pHZ3RkVjAzT05odzhXNm5DWFdwOHMycHJxR1J6d1pSbzJNWnN5M3MtbkV3S1lSbDJUczBBajB6U2x2Uw?oc=5
- [1] Israel boosts David's Sling capabilities to withstand weeks of missile attacks | The Jerusalem Post | https://news.google.com/rss/articles/CBMiY0FVX3lxTE5hc1luX2VwM0o0Ym4zR2xOSEZsWDltaVhjSWhuM1ZiX2xWdUNHamxMUS1RX19FeXVXWHFuMy02QjMxYVFQYWtKV0cxd2ZLS05TbnJDc09WeW81aUFxREZXeC12WQ?oc=5
- [1] Clock ticking on Iran strike as Tehran races to fortify nuclear sites | Ynetnews | https://news.google.com/rss/articles/CBMibkFVX3lxTE9WdGlQNHFfQjhjZWhVQXZyZ0cwTVVReW1ySG9nOGRDQU5vZFg3cGFBX3Q4MlJESTZybHhMRE9Nc2NsYXBxdXZFdDgxV2dNSkE3X2drQkswTWpIVjhjem5ZVlMtTWNmejlRUlVrOWhB?oc=5
- [1] Analysis • Netanyahu's failed coup makes him all the keener on reigniting the Iranian front | Haaretz | https://news.google.com/rss/articles/CBMipAJBVV95cUxQUU0yNFNZWEhlMmlSQmhDQnVsS19KLWhxeHRlRHkxeUlNV2pfc1FrNndqczFZX2pmaV9QckFJM3paLWJVZHdUZjJWbnRuTlBqMjFWbGVUR2VNZ2JDeXJabFVfNGhUWjJxbXFwUk9kcFR3aDhCZHdtY19GblQzVDJNZ2tBZHZ4T2E2aksxT3BXQjBBQzdLOEVhTFRBYmdPT0dVVXphaXpqYjBOcThHckMwSnl3cXNrTmcxZk9kcE9HVzZDdV9rUUVuT1AwQnVXa1JjM2F5NlVDOWNORUtQZVAwZy1Tb3dCTUlVTEt4aU1PSUVpaUtQQU5FQ2d1YmVybUk2akRnT3VIZy1XVnVYTFdNTGZjdWFCbWUyRHpOeTRxV0x2ZXpS?oc=5
- [1] How the war in Iran turned the Gulf into a climate catastrophe – video explainer | The Guardian | https://news.google.com/rss/articles/CBMiygFBVV95cUxOSm9fUVhKMnFodGZaRFVuLUQ0c0ZQWFM2eUhBREhxdURNVjIxU0EycTZpX0RTMU9Od3BMcWNFZmtRaTQ3M3N0M3dMUUpOTUJxZWE1SDg4MEQ2b21rSzhsT25kNWNuWXhjd1p3RW1ubkVFcHhrQklFcmd0S3V6M1RfSjdESGlHamZfWHVHUWpySlBiMHhXdVhid213NFRsMkdhT05BV0YzQ05QVkRGS1FmQ1J4Wk0zRGt0cUpNbHNmVHlvallpV1BVbHZ3?oc=5
- [1] Iran’s Top Ally Has 20-Year Grudge Against Man Who May Oust Netanyahu | Newsweek | https://news.google.com/rss/articles/CBMipAFBVV95cUxQM1NIYW1SeGhsd3RxSHUzaDB4NmY0VUpUU0Z1aUh2T1I3QUFyZkVveWJMLV82dFI3S2hRT05VLXF4YzkyZ0ZOTXdXTC1Rd2NxQVpHeVJ6dGRCakRhYlhnZXR5bGpVWFYzVHl3UmZ3WFQ5V3F2bDRNTV9HT1BDYzhwdTRQRnpmWmwtOUxpMk9pV2VNcVFQTzFmZG1XV0R4U0R5VVBNNg?oc=5
- [1] US Senate Rejects Bid To Curb Trump’s War Powers On Iran | LIVE BLOG | i24NEWS | https://news.google.com/rss/articles/CBMiwwFBVV95cUxQM2E0TFQwV1hDay1UczE4ajUzRW9NaE0xWjJnSVFHRGdCVnhKeVhlREJsNHpsanhrbjB3VHB3SUZ6RWJYSTMtczdNeWZyNW95QzBPU1NiYkFDSy1zZEROclRQU25KcW1NdXZwWGJmT3RNZmFkQTNLMWRsQldBRnliV2ZwbUZxMHJLLXRqamtvNlRLSXRlUDZXZm9WeFljUGFaeFF1ODZZdk05WTIzUHB3OWN1WFF6TWZvU24wWkNDVkNhV0E?oc=5
- [1] Israel Upgrades David's Sling as $1 Million Interceptors Counter Iran's Saturation Missile Attacks | BigGo Finance | https://news.google.com/rss/articles/CBMidkFVX3lxTE1VMnpkYTNTQkZkM0ZNQkRuV2hkZk40Q05SMVc2VDFwQVJ0c3JUZjlWMXZndG9HVjV0MEwweHNBUDVsZ1lOdTR5TVJYdFVMcG9wQk0zT05lTDlHRG1YdVNWQTl5Mk5ISC1lTjJHc3VXS0RvaE11Mmc?oc=5
- [1] Netanyahu using Iran threat to obstruct Eisenkot government bid, Israeli analysts say | Anadolu Ajansı | https://news.google.com/rss/articles/CBMiyAFBVV95cUxPakgydklJM0lKOGJPWnNmV29oVnRyX2NXRnF4MERwZFdlcW5GOFhGR2wtLVVUb3dVajJvdmwybnRXVkpQNjFranZDUWVoSzZrN29ETnVNZkpxeXc3NlZ6bk1QMW85dy1XeWl6bi15WUZTbmw2YldOYTJReERkb1dtTEdpUERRUW9XeHhkT1FaSHo1Rnd6X0kxZU9FMGJzYVMwQXo0cWVaWnRRdlRZTGFDTU9lTmtram9lUlBwbmEyVTkwa1ExeHVJcA?oc=5
- [1] Will the US and Israel restart the war on Iran? | Middle East Eye | https://news.google.com/rss/articles/CBMilwFBVV95cUxNQVZyMWZUUklQRGpJa2pHZUJNbElIWHp2MVdfaGlkdlpOZFJoMnM5NjNxUDNsTGh6MGpxQjVfd3JOXzBFVFFHUUlicDNVOXlEeDlqN1pfd0pTYjM3dFpPM2FCaXhfVVBMMTJjVGxWTVFPSFlLS2xVRk5fV0NnTUROT1FUdDJiMnpVc0hXOHp5bDBSbXhRSlFV?oc=5

## geo (auto-located kinetic reports, UNVERIFIED keyword+place match; check date/source; conf u unless confirmed)
- 2026-11-20T12:59:04Z تنگه هرمز (26.57,56.25) explosion x2 news:Marine Insight: Global Oil Prices Rise After Reports On Hormuz Tanker Blasts And Houthi Attack On Saudi Capital https://news.google.com/rss/articles/CBMiiAFBVV95cUxOaVh4Mk9Jb3Z5ZjdEYjNTbTNuUThKWEJpeTB1WGZkUUpDQ2ozbVAtYThHLTdzbmJxd19iS1RVZjVGTVRxcVdubVp6el9fUm9UbGhXRktiOUt5SldiamUtVk0tQTNfTUQ1RnNDaVQ0ZlN2Y1E0ampWOUZIT1RhclJRV3NBcFJLdVdY?oc=5
- 2026-11-20T12:46:57Z جده (21.49,39.19) strike x7 tg:isna94: سخنگوی ارتش یمن: اگر بندر الحدیده بمباران شود تمام بنادر عربستان را هدف قرار می‌دهیم 🔹 ما از تمام کارمندان و کارکنان بندر جده و تمام بنادر عربستان می‌خواهیم فور https://t.me/isna94/414370
- 2026-11-20T12:46:42Z مشهد (36.3,59.6) drone x2 tg:shin_persian: Shin ✓ @hey_itsmyturn UAV seen in the sky over Mashhad. Razavi Khorasan Province, Iran [Delayed Post via FromIran · 120-second delay] https://fromiran.sh1n.org/ https://t.me/shin_persian/12631
- 2026-11-20T12:38:17Z تهران (35.69,51.39) missile x1 tg:shin_persian: Shin ✓ @hey_itsmyturn 16:00 local | 1230Z Missile launch from Abadan Khuzestan Province, Iran [Delayed Post via FromIran · 120-second delay] https://fromiran.sh https://t.me/shin_persian/12629
- 2026-11-20T12:35:41Z قشم (26.95,56.27) explosion x1 tg:alibk3: سماع دوي انفجار في جزيرة قشم قبل قليل نتيجة إطلاق صاروخي https://t.me/alibk3/41940
- 2026-11-20T12:32:50Z تهران (35.69,51.39) strike x1 tg:mehrnews: دیوارنگاره جدید تامل بدانگیز میدان جهاد تهران به مناسبت روز کودک: آمریکا ۱۶۸ کودک ایرانی را در میناب کشته است 🔺 همزمان با روز کودک از جدیدترین دیوارنگاره میدان  https://t.me/mehrnews/433613
- 2026-11-20T12:32:17Z قشم (26.95,56.27) missile x1 tg:shin_persian: Shin ✓ @hey_itsmyturn Missile launched from Qeshm. Hormozgan Province, Iran [Delayed Post via FromIran · 120-second delay] https://fromiran.sh1n.org/incidents/S https://t.me/shin_persian/12628
- 2026-11-20T12:25:20Z اصفهان (32.65,51.67) fighter x1 tg:shin_persian: Shin ✓ @hey_itsmyturn Jet activity heard in Qahjavarestan, Isfahan Isfahan Province, Iran [Delayed Post via FromIran · 120-second delay] https://fromiran.sh1n.o https://t.me/shin_persian/12626
- 2026-11-20T08:53:29Z تنگه هرمز (26.57,56.25) strike x1 tg:shin_persian: Martin Kelly ✓ @_MartinKelly_ This week in numbers: 15 merchant vessels attacked in seven days Attacks on shipping rose 50% this week, to the highest weekly tot https://t.me/shin_persian/12620
- 2026-11-20T06:47:28Z اصفهان (32.65,51.67) air_defense x1 tg:shin_persian: Shin ✓ @hey_itsmyturn AA fire heard in Baharestan, Isfahan. Isfahan Province, Iran [Delayed Post via FromIran · 120-second delay] https://fromiran.sh1n.org/inci https://t.me/shin_persian/12617
- 2026-11-20T06:47:09Z دزفول (32.38,48.4) fighter x1 tg:shin_persian: Shin ✓ @hey_itsmyturn Jet activity heard in Dezful. Khuzestan Province, Iran [Delayed Post via FromIran · 120-second delay] https://fromiran.sh1n.org/incidents/ https://t.me/shin_persian/12616
- 2026-11-20T06:20:58Z اصفهان (32.65,51.67) uxo/explosion x1 tg:shin_persian: Shin ✓ @hey_itsmyturn Blast due to UXO disposal in Baharestan, Isfahan. Isfahan Province, Iran [Delayed Post via FromIran · 120-second delay] https://fromiran.s https://t.me/shin_persian/12614
- 2026-11-19T22:11:50Z تهران (35.69,51.39) strike x1 news:Israel National News, The Jerusalem: "Holy S-, that’s Tehran": B-2 pilots reveal dramatic moments of strikes on nuclear sites https://news.google.com/rss/articles/CBMiWkFVX3lxTFBKX01iRnpNOFhid1hTbFZsb2VfY2YzbXNQNXNfZDE1RkwxdG1GU1A5clFVeW9iWWdSN2RIOUdhbncybnZDY1dRNmdoOFRkZ1EwNFlMcEdGQjBEQQ?oc=5

## telegram (relevant)
- 2026-11-20T13:00:20Z @bbcpersian: دو مرد بریتانیایی که به همکاری با یک سرویس اطلاعاتی خارجی در ارتباط با توطئه احتمالی علیه پایگاه هوایی فرفورد متهم شده‌اند، از طریق ارتباط ویدیویی در دادگاه اولد بیلی لندن حاضر شدند و هر دو نفر، اتهام https://t.me/bbcpersian/295775
- 2026-11-20T12:59:58Z @irna_1313: #اختصاصی 🎥 سردار بلالی: دست‌به‌ماشه آماده‌ایم/توان موشکی ایران محدودیت ندارد مشاور عالی فرمانده نیروی هوافضای سپاه: 🔹 نیروهای مسلح در آمادگی کامل قرار دارند و دست به ماشه، منتظر هرگونه خطای محاسباتی و https://t.me/irna_1313/476142
- 2026-11-20T12:59:05Z @indypersian: ♦️ فرماندهی نیروهای مشترک ائتلاف به رهبری عربستان سعودی، روز جمعه ۲۹ آبان از غیرنظامیان خواست برای حفظ جان خود، بندر حدیده در یمن را تخلیه کنند. این فرماندهی با انتشار اطلاعیه‌ای در شبکه‌ اجتماعی ایکس https://t.me/indypersian/183220
- 2026-11-20T12:57:03Z @yediotnews25: דיווח בCBS: ״ישראל וארה״ב שוקלות לתקוף באיראן בטווח הזמן הקרוב״ https://t.me/yediotnews25/138250
- 2026-11-20T12:56:11Z @akhbarefori: 🔴 یمن: فورا آن را تخلیه کنید| در پاسخ به حملۀ عربستان به ایستگاه برق صعده و المخا، ایستگاه برق الشقیق را تا ساعاتی بعد هدف قرار می‌دهیم 🔹 اعلام می‌کنیم که مرکز مالی شهر اقتصادی ملک عبدالله در ریاض، هد https://t.me/akhbarefori/708688
- 2026-11-20T12:55:41Z @warmonitors: ⚡ #BREAKING Saudi Civil Defense: An alert was issued in the Jazan region to warn of a danger. 💧 Rainbet.com the #1 Non-KYC Crypto Casino & Sportsbook @rainbetcom +18 https://t.me/warmonitors/46776
- 2026-11-20T12:55:27Z @ynetalerts: 🔴 ‏דיווח ב-CBS: "ישראל וארה"ב שוקלות לפתוח במתקפה חדשה נגד איראן בטווח הזמן הקרוב" למבזק המלא ב-ynet > https://t.me/ynetalerts/78369
- 2026-11-20T12:55:00Z @bbcpersian: 🔻 محاکمه دو بریتانیایی به اتهام همکاری با یک سرویس اطلاعاتی خارجی در ارتباط با پایگاه هوایی فرفورد ✍️ ژیار گل، دادگاه اولد بیلی لندن دو مرد بریتانیایی که به همکاری با یک سرویس اطلاعاتی خارجی در ارتباط https://t.me/bbcpersian/295774
- 2026-11-20T12:53:46Z @mehrnews: 🏫 همزمان با آخرین روز نمایشگاه بین‌المللی بورس، بانک و بیمه برگزار شد 🖌 آیین قدردانی از اعتماد ۱۰ میلیونی مشتریان به چکنوی بانک صادرات ایران/ کسب رتبه نخست شبکه بانکی از نظر صدور چک امن دیجیتال 🏫 آیین https://t.me/mehrnews/433621
- 2026-11-20T12:51:07Z @isna94: عزیزی، رئیس کمیسیون امنیت ملی: ایران قابل محاصره نیست @isna94 https://t.me/isna94/414375
- 2026-11-20T12:49:56Z @mehrnews: نیروهای مسلح یمن تصاویری از اهداف بعدی خود منتشر کردند 🔗 mehrnews.com 📡 @Mehrnews https://t.me/mehrnews/433616
- 2026-11-20T12:49:26Z @jamarannews: 🔴 گزارش جماران 🔴 از لیبی تا ایران؛ سابقه ۲۹ ساله ادعاهای خطرناک نیویورک‌تایمز درباره زیرساخت‌های حیاتی آب 🔴 پروژه آبی لیبی که «مشکوک به کاربری نظامی» معرفی شد، ۱۴ سال بعد هدف حمله ناتو قرار گرفت 🔻 برر https://t.me/jamarannews/562352
- 2026-11-20T12:48:18Z @irna_1313: دو متهم پرونده «فرفورد» اتهامات امنیتی انگلیس را رد کردند 🔹 دو متهم پرونده پایگاه هوایی فرفورد انگلیس که مقام‌های این کشور مدعی ارتباط آن با ایران هستند، اتهامات امنیتی علیه خود را رد کردند. #ایرنا_جه https://t.me/irna_1313/476140
- 2026-11-20T12:48:01Z @presstv: Iran has ‘fingers on trigger’ to respond to enemy miscalculation: IRGC aide An advisor to the commander of the IRGC Aerospace Force warns that Iranian Armed Forces remain at the highest level of readi https://t.me/presstv/215489
- 2026-11-20T12:47:41Z @clashreport: NEW: The U.S. and Israel are considering a new assault on Iran in the near term. Netanyahu favors a joint operation, but Trump remains undecided. Source: CBS News https://t.me/clashreport/106958
- 2026-11-20T12:46:57Z @isna94: سخنگوی ارتش یمن: اگر بندر الحدیده بمباران شود تمام بنادر عربستان را هدف قرار می‌دهیم 🔹 ما از تمام کارمندان و کارکنان بندر جده و تمام بنادر عربستان می‌خواهیم فورا آنجا را تخلیه کنند. 🔹 از تمام شرکت‌های https://t.me/isna94/414370
- 2026-11-20T12:46:42Z @shin_persian: Shin ✓ @hey_itsmyturn UAV seen in the sky over Mashhad. Razavi Khorasan Province, Iran [Delayed Post via FromIran · 120-second delay] https://fromiran.sh1n.org/incidents/mYfbi4N5Bj4jJ_o8KAL5eSfT ترجمه https://t.me/shin_persian/12631
- 2026-11-20T12:46:40Z @shin_persian: Shin ✓ @hey_itsmyturn UAV seen in the sky over Mashhad. Razavi Khorasan Province, Iran [Delayed Post via FromIran · 120-second delay] https://fromiran.sh1n.org/incidents/mYfbi4N5Bj4jJ_o8KAL5eSfT ترجمه https://t.me/shin_persian/12630
- 2026-11-20T12:45:28Z @jamarannews: 🔴 نیروهای مسلح یمن تصاویری از اهداف بعدی خود منتشر کردند 🔴 انصار الله یمن اعلام کرد: در پاسخ به هدف قرار دادن دو نیروگاه برق «صعده» و «المخا» از سوی دشمن سعودی، اعلام می‌کنیم که نیروگاه برق «الشقیق» د https://t.me/jamarannews/562347
- 2026-11-20T12:45:25Z @farsna: ‌ 🔴 مرکز مالی شهر اقتصادی عربستان هدف بعدی یمن 🔹 یحیی سریع: اعلام می‌کنیم که مرکز مالی شهر اقتصادی ملک عبدالله در ریاض، هدف نظامی نیروهای ما است. 🔹 بنابراین، از تمام کارکنان، کارمندان و شهروندان تقاضا https://t.me/farsna/475679
- 2026-11-20T12:44:25Z @akhbarefori: ♦️ توئیت معنادار رئیس کمیسیون امنیت ملی: ایران محاصره‌پذیر نیست 🇮🇷 ✊ @AkhbareFori | Link https://t.me/akhbarefori/708685
- 2026-11-20T12:43:30Z @jamarannews: 🔴 عربستان نیروگاه‌های برق یمن را بمباران می‌کند 🔻 العربی الجدید گزارش داد که نیروگاه‌های برق هدف جدید عربستان در یمن برای بمباران است و تا کنون دو نیروگاه برق از جمله نیروگاه برق شهر المخا و در ساحل د https://t.me/jamarannews/562346
- 2026-11-20T12:42:53Z @isna94: حمله به یک کشتی در سواحل عمان 🔹 منابع خبری از حمله به یک کشتی در سواحل عمان خبر دادند. 🔹 پیش از این صابرین نیوز از وقوع انفجارهایی در تنگه هرمز و هدف قرار گرفتن یک کشتی در این تنگه خبر داده بود. 🔹 برخ https://t.me/isna94/414369
- 2026-11-20T12:41:15Z @rotternews: רשת CBS: ישראל וארה״ב שוקלות לפתוח במתקפה נוספת נגד איראן בזמן הקרוב 📰 לאשכול המלא 📰 https://t.me/rotternews/371795
- 2026-11-20T12:40:38Z @warmonitors: ⚡ Russian missile crash in Poland likely an intentional provocation as European militaries hold drills, Polish leader says. 💧 Rainbet.com the #1 Non-KYC Crypto Casino & Sportsbook @rainbetcom +18 https://t.me/warmonitors/46775
- 2026-11-20T12:39:58Z @irna_1313: دموکرات‌ها و تهیه پیش‌نویس طرح محدودیت بودجه جنگ علیه ایران 🔹️ تارنمای نشریه پولیتیکو نوشت: گروهی از دموکرات‌های کنگره در قالب بخشی از یک توافق بودجه ای برای اجتناب از تعطیلی دولت در سه هفته آتی مشغول https://t.me/irna_1313/476139
- 2026-11-20T12:39:24Z @mehrnews: فراخوان رسانه‌ای «جان‌فدا» در تهران آغاز شد 🔺 معاون روابط‌عمومی سپاه حضرت محمد رسول‌الله (ص) تهران بزرگ از آغاز فراخوان جذب و آموزش نیروهای متخصص «جان فدا» در حوزه‌های مختلف رسانه‌ای خبر داد. 🔺 وی اظه https://t.me/mehrnews/433615
- 2026-11-20T12:38:17Z @shin_persian: Shin ✓ @hey_itsmyturn 16:00 local | 1230Z Missile launch from Abadan Khuzestan Province, Iran [Delayed Post via FromIran · 120-second delay] https://fromiran.sh1n.org/incidents/49S7MJEDFbWmpefh9mHfnK8 https://t.me/shin_persian/12629
- 2026-11-20T12:37:44Z @N12chat: אסף רוזנצוייג על רקע דיווחים כי איראן מטעינה מכליות נפט ונערכת לפרוץ את המצור של ארה"ב, ראש הוועדה לביטחון לאומי בפרלמנט של איראן אברהאים עזיזי כותב בצירוף שעון חול וחבית נפט: "לא ניתן להטיל מצור על א https://t.me/N12chat/236096
- 2026-11-20T12:37:41Z @N12chat: אסף רוזנצוייג מפקד משמרות המהפכה אחמד וחידי אמר כי פעולותיהן של ארה"ב וישראל עשויות להביא לשינוי בדוקטרינת ההגנה של איראן. בתשובה לשאלה על האפשרות להגדיל את טווח הטילים האיראניים ולבצע תקיפות ללא מגבל https://t.me/N12chat/236095
- 2026-11-20T12:37:15Z @N12chat: אסף רוזנצוייג על רקע דיווחים כי איראן מטעינה מכליות נפט ונערכת לפרוץ את המצור של ארה"ב, ראש הוועדה לביטחון לאומי בפרלמנט של איראן אברהאים עזיזי כותב בצירוף שעון חול וחבית נפט: "לא ניתן להטיל מצור על א https://t.me/N12chat/236094
- 2026-11-20T12:36:01Z @presstv: 🔴 Ebrahim Azizi, Chairman of the National Security Committee of the Iranian Parliament on X: Iran cannot be blockaded. 🛢 ⏳ @PressTV https://t.me/presstv/215488
- 2026-11-20T12:35:41Z @alibk3: سماع دوي انفجار في جزيرة قشم قبل قليل نتيجة إطلاق صاروخي https://t.me/alibk3/41940
- 2026-11-20T12:35:37Z @mehrnews: 📹 جام رسانه امید؛ گردهمایی ۳۱۳ فعال رسانه‌ای از سراسر کشور با حضور نمایندگانی از ۱۲ کشور 🔺 مرتضی کارآموزیان مسئول سازمان بسیج رسانه و روح‌الله رحمانی دبیر علمی و محتوایی رویداد جام رسانه امید، در گفت‌ https://t.me/mehrnews/433614
- 2026-11-20T12:35:33Z @akhbarefori: 🔴 منابع خبری از حمله به یک کشتی در سواحل عمان خبر دادند 📲 🇮🇷 ✊ @AkhbareFori | Link https://t.me/akhbarefori/708683
- 2026-11-20T12:32:50Z @mehrnews: دیوارنگاره جدید تامل بدانگیز میدان جهاد تهران به مناسبت روز کودک: آمریکا ۱۶۸ کودک ایرانی را در میناب کشته است 🔺 همزمان با روز کودک از جدیدترین دیوارنگاره میدان جهاد تهران با شعار " میناب را به یاد آور https://t.me/mehrnews/433613
- 2026-11-20T12:32:20Z @jamarannews: 🔴 تریتا پارسی: ایران در حال شکستن محاصره دریایی است 🔻 تریتا پارسی نوشت: به نظر می‌رسد اکنون ایران در حال برداشتن گامی بزرگ در راستای تغییر وضع موجود به نفع خود است و می‌خواهد بر خلاف محاصره دریایی اعم https://t.me/jamarannews/562345
- 2026-11-20T12:32:17Z @shin_persian: Shin ✓ @hey_itsmyturn Missile launched from Qeshm. Hormozgan Province, Iran [Delayed Post via FromIran · 120-second delay] https://fromiran.sh1n.org/incidents/SgCfw9TqdMnZIlOtSlHC6ngC ترجمه خودکار فار https://t.me/shin_persian/12628
- 2026-11-20T12:31:43Z @idfofficial: IDF: Winter preparedness efforts in Gaza continue: More than 7,000 tents and hundreds of trucks carrying winter supplies were brought in this week alone The IDF and COGAT continue to proactively coord https://t.me/idfofficial/19509
- 2026-11-20T12:31:41Z @iranintltv: یک شهروند با ارسال ویدیویی به ایران اینترنشنال، اقلام خریداری‌شده با اعتبار دو میلیون تومانی کالابرگ تیرماه برای دو نفر را نشان داد و از کاهش قدرت خرید و سیاست‌های حکومت انتقاد کرد. او گفت جمهوری اسلا https://t.me/iranintltv/367882
- 2026-11-20T12:30:21Z @akhbarefori: ♦️ توئیت معنادار رئیس کمیسیون امنیت ملی: ایران محاصره‌پذیر نیست 🇮🇷 ✊ @AkhbareFori | Link https://t.me/akhbarefori/708682
- 2026-11-20T12:30:01Z @akhbarefori: ♦️ نمایشگاه مایکروسافت یا سیتکس تهران؟! 🔹 ویدیویی از تعطیلی نمایشگاه مایکروسافت و متا بدلیل بارش باران و آب‌دادن سقف نمایشگاه و مقایسه آن با نمایشگاه سیتکس تهران در فضای مجازی پربازدید شده است. 🇮🇷 ✊ @ https://t.me/akhbarefori/708681
- 2026-11-20T12:28:47Z @shin_persian: Shin ✓ @hey_itsmyturn The new command in Jurf al-Sakhar is open. The forces are at the gates. They've surrounded it on all sides. IRGC-backed Kataib Hezballah's line: "we will not leave even if govern https://t.me/shin_persian/12627
- 2026-11-20T12:28:34Z @akharinkhabar: 📸 توئیت معنادار رئیس کمیسیون امنیت ملی: ایران محاصره‌پذیر نیست 🔹 همزمان منابع غیررسمی از پایان صبر ایران مقابل محاصره دریایی خبر می‌دهند. @Akharinkhabar | akharinkhabar.ir https://t.me/akharinkhabar/645729
- 2026-11-20T12:27:58Z @irna_1313: تهران و اسلام‌آباد حامیان صف اول فلسطین هستند/محکومیت عملیات نظامی اسرائیل 🔹 سخنگوی وزارت امور خارجه پاکستان در واکنش به درخواست وزیر امور خارجه جمهوری اسلامی ایران برای برگزاری نشست اضطراری سازمان هم https://t.me/irna_1313/476137
- 2026-11-20T12:27:00Z @akharinkhabar: 🔺 🔻 اختلاف بر سر جنگ با ایران، تعطیلی دولت آمریکا را محتمل کرد 🔹 اختلافات دو حزب در کنگره آمریکا بر سر جنگ علیه ایران و درخواست ترامپ برای اختصاص ۳۵۰ میلیارد دلار بودجه اضافی به پنتاگون، تلاش‌ها برای  https://t.me/akharinkhabar/645728
- 2026-11-20T12:26:01Z @presstv: 🔴 Yemeni Armed Forces spokesperson Yahya Saree warns airlines that Saudi airspace, except over Mecca and Medina, is unsafe and could become the scene of Yemeni operations within hours. 🔺 Yemen will ta https://t.me/presstv/215487
- 2026-11-20T12:25:20Z @shin_persian: Shin ✓ @hey_itsmyturn Jet activity heard in Qahjavarestan, Isfahan Isfahan Province, Iran [Delayed Post via FromIran · 120-second delay] https://fromiran.sh1n.org/incidents/N8iw_nUfLBG8BAobuJK4p0jW تر https://t.me/shin_persian/12626
- 2026-11-20T12:23:36Z @iranintltv: محمدعلی ابطحی، فعال سیاسی اصلاح‌طلب، گفت که سازمان اطلاعاتی موساد پشت جریان‌های تندرو و تلاش‌ها برای برکناری مسعود پزشکیان است. ابطحی افزود: «سازمانی که توانایی شناسایی محل خواب فرماندهان را دارد، می‌ https://t.me/iranintltv/367881
- 2026-11-20T12:23:02Z @geopolitics_prime: 🇮🇷 🚀 Iran’s increasingly sophisticated missiles expose limits of Israel’s costly air defenses Iran’s Operation True Promise-series missile and drone counterstrikes have put Israel’s interceptor stockp https://t.me/geopolitics_prime/78053
