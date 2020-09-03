from collections import defaultdict

FN_PAIRS = [('allar', 'PBFPN'),
            ('allir', 'PBMPN'),
            ('alt', 'PBNPN'),
            ('alt', 'PBNSN'),
            ('annan', 'PBMSA'),
            ('annar', 'PBMSN'),
            ('annað', 'PBNSN'),
            ('aðrar', 'PBFPN'),
            ('aðrir', 'PBMPN'),
            ('báðir', 'PBMPN'),
            ('bæði', 'PBNPN'),
            ('ein', 'PBFSN'),
            ('eg', 'PP1SN'),
            ('ein', 'PBMSA'),
            ('ein', 'PBMSN'),
            ('ein', 'PBNSN'),
            ('eina', 'PBFSA'),
            ('einar', 'PBFPN'),
            ('eingi', 'PBNPN'),
            ('eingin', 'PBFSN'),
            ('eingin', 'PBMSN'),
            ('eini', 'PBFSD'),
            ('eini', 'PBNSD'),
            ('eini', 'PBNSN'),
            ('einir', 'PBNPN'),
            ('einki', 'PBNSN'),
            ('einum', 'PBMSD'),
            ('eitt', 'PBNSA'),
            ('eitt', 'PBNSN'),
            ('handan', 'PDFSN'),
            ('hann', 'PMSN'),
            ('hansara', 'PMSG'),
            ('hasar', 'PDMPA'),
            ('hatta', 'PDNSN'),
            ('henda', 'PDFSN'),
            ('henda', 'PDMSA'),
            ('hendan', 'PDFSA'),
            ('hendan', 'PDFSN'),
            ('hendan', 'PDMSA'),
            ('henni', 'PFSD'),
            ('hesa', 'PDFSA'),
            ('hesar', 'PDFPA'),
            ('hesar', 'PDFPN'),
            ('hesi', 'PDNPA'),
            ('hesi', 'PDNPN'),
            ('hesin', 'PDMSN'),
            ('hesir', 'PDMPN'),
            ('hesum', 'PDNPD'),
            ('hesum', 'PDNSD'),
            ('hetta', 'PDFPN'),
            ('hetta', 'PDNPN'),
            ('hetta', 'PDNSA'),
            ('hetta', 'PDNSN'),
            ('hin', 'PDFSN'),
            ('hin', 'PDMSN'),
            ('hini', 'PDNPN'),
            ('hinir', 'PDMPN'),
            ('hon', 'PFSN'),
            ('honum', 'PMSD'),
            ('hvat', 'PNSA'),
            ('hvat', 'PNSN'),
            ('hvør', 'PBMSN'),
            ('hvør', 'PMSN'),
            ('hvørja', 'PFSA'),
            ('hvørjar', 'PMPN'),
            ('hvørji', 'PBNPA'),
            ('muslimskar', 'PBFPN'),
            ('mær', 'PP1SD'),
            ('mín', 'PP1SN'),
            ('mítt', 'PP1SG'),
            ('nakað', 'PBNSN'),
            ('nakrar', 'PBFPN'),
            ('nakrar', 'PBMPA'),
            ('nakrir', 'PBMPN'),
            ('nógv', 'PBNPN'),
            ('nøkur', 'PBNPN'),
            ('okkara', 'PP1PG'),
            ('okkurt', 'PBNSA'),
            ('okkurt', 'PBNSN'),
            ('ongar', 'PBFPN'),
            ('ongin', 'PBFSN'),
            ('ongin', 'PBMSN'),
            ('onkrir', 'PBMPN'),
            ('onkur', 'PBFSN'),
            ('onkur', 'PBMSN'),
            ('onlur', 'PBMSN'),
            ('onnur', 'PBFSN'),
            ('onnur', 'PBNPN'),
            ('summi', 'PBNPN'),
            ('summir', 'PBMPN'),
            ('ta', 'PDFSA'),
            ('tann', 'PDFSN'),
            ('tann', 'PDMSA'),
            ('tann', 'PDMSN'),
            ('tað', 'PDNSN'),
            ('tað', 'PNSA'),
            ('tað', 'PNSN'),
            ('teimum', 'PNPD'),
            ('teir', 'PDMPN'),
            ('teir', 'PMPN'),
            ('teirra', 'PNPG'),
            ('tess', 'PNSG'),
            ('tey', 'PDNPA'),
            ('tey', 'PDNPN'),
            ('tey', 'PNPN'),
            ('tit', 'PP2PN'),
            ('tygara', 'PP2PG'),
            ('tær', 'PDFPN'),
            ('tær', 'PFPN'),
            ('tú', 'PP2SN'),
            ('vit', 'PP1PN'),
            ('alla', 'PBFSA'),
            ('alla', 'PBNSA'),
            ('allan', 'PBMSA'),
            ('allar', 'PBFPA'),
            ('allar', 'PBFSN'),
            ('allar', 'PBMPA'),
            ('allar', 'PFPN'),
            ('allari', 'PBFSD'),
            ('alt', 'PBNPA'),
            ('alt', 'PBNSA'),
            ('alt', 'PNSA'),
            ('annan', 'PBNSA'),
            ('annað', 'PBNSA'),
            ('aðra', 'PBFSA'),
            ('aðrar', 'PBFPA'),
            ('aðrar', 'PBMPA'),
            ('aðrari', 'PBFSD'),
            ('aðrir', 'PMPN'),
            ('aðru', 'PBFSA'),
            ('aðru', 'PBFSD'),
            ('báðar', 'PBFPA'),
            ('báðar', 'PBFPN'),
            ('báðar', 'PBMPA'),
            ('báðu', 'PBFPA'),
            ('báðum', 'PBFPD'),
            ('báðum', 'PBMPD'),
            ('báðum', 'PBNPD'),
            ('bæði', 'PBNPA'),
            ('ein', 'PBFSA'),
            ('ein', 'PBNPN'),
            ('ein', 'PBNSA'),
            ('eina', 'PBFSN'),
            ('eina', 'PBMSA'),
            ('einar', 'PBFPA'),
            ('einar', 'PBMPA'),
            ('einari', 'PBFSD'),
            ('eingi', 'PBNPA'),
            ('eingin', 'PBNSN'),
            ('eingir', 'PBMPN'),
            ('eini', 'PBFSA'),
            ('eini', 'PBNPA'),
            ('eini', 'PBNPN'),
            ('eini', 'PBNSA'),
            ('einir', 'PBMPN'),
            ('einki', 'PBNPN'),
            ('einki', 'PBNSA'),
            ('einki', 'PNSN'),
            ('einum', 'PBNPD'),
            ('einum', 'PBNSD'),
            ('eitt', 'PBFSA'),
            ('eitthvørt', 'PBNSA'),
            ('eitthvørt', 'PBNSN'),
            ('hana', 'PPFSA'),
            ('hann', 'PPMSA'),
            ('hann', 'PPMSN'),
            ('hansara', 'PPMSG'),
            ('hasi', 'PDNPA'),
            ('hasi', 'PDNPN'),
            ('hasin', 'PDMSN'),
            ('hasum', 'PDMPD'),
            ('hasum', 'PDNPD'),
            ('hasum', 'PDNSD'),
            ('hatta', 'PDNSA'),
            ('hennara', 'PPFSG'),
            ('henni', 'PPFSD'),
            ('hesar', 'PDMPA'),
            ('hesari', 'PDFSD'),
            ('hesi', 'PDFSD'),
            ('hesum', 'PDFPD'),
            ('hesum', 'PDMPD'),
            ('hesum', 'PDMSD'),
            ('hin', 'PDMSA'),
            ('hinar', 'PDFPA'),
            ('hinar', 'PDFPN'),
            ('hinar', 'PDMPA'),
            ('hini', 'PDNPA'),
            ('hinir', 'PBMPN'),
            ('hinum', 'PDFPD'),
            ('hinum', 'PDMPD'),
            ('hinum', 'PDMSD'),
            ('hinum', 'PDNPD'),
            ('hinum', 'PDNSD'),
            ('hitt', 'PDNSA'),
            ('hitt', 'PDNSN'),
            ('hon', 'PPFSN'),
            ('honum', 'PPMSD'),
            ('hvønn', 'PBMSA'),
            ('hvønn', 'PBNSA'),
            ('hvønn', 'PBNSN'),
            ('hvønn', 'PMSA'),
            ('hvønnannan', 'PBMPD'),
            ('hvønnannan', 'PBMSA'),
            ('hvør', 'PBFSN'),
            ('hvør', 'PBNPA'),
            ('hvør', 'PBNPD'),
            ('hvør', 'PBNSN'),
            ('hvør', 'PFSD'),
            ('hvør', 'PFSN'),
            ('hvørgin', 'PBMSN'),
            ('hvørjar', 'PBMPA'),
            ('hvørjar', 'PFPA'),
            ('hvørjar', 'PFPN'),
            ('hvørjari', 'PBFSD'),
            ('hvørji', 'PBFPN'),
            ('hvørji', 'PBFSD'),
            ('hvørji', 'PBNPN'),
            ('hvørji', 'PBNSA'),
            ('hvørjir', 'PMPN'),
            ('hvørjum', 'PBFPD'),
            ('hvørjum', 'PBMSD'),
            ('hvørjum', 'PBNSD'),
            ('hvørjum', 'PMSD'),
            ('hvørjum', 'PNSD'),
            ('hvørt', 'PBNSA'),
            ('hvørt', 'PBNSN'),
            ('hvørt', 'PNSA'),
            ('lokalir', 'PBMPN'),
            ('man', 'PBNSN'),
            ('mann', 'PBNSN'),
            ('meg', 'PP1SA'),
            ('mong', 'PBNPN'),
            ('mín', 'PP1SA'),
            ('míni', 'PP1PA'),
            ('míni', 'PP1PN'),
            ('míni', 'PP1SD'),
            ('mínum', 'PP1PD'),
            ('mínum', 'PP1SD'),
            ('mítt', 'PP1SA'),
            ('nakar', 'PBMSN'),
            ('nakar', 'PBNSN'),
            ('nakað', 'PBNSA'),
            ('nakra', 'PBFSA'),
            ('nakran', 'PBMSA'),
            ('nakrar', 'PBFPA'),
            ('nakrari', 'PBFSD'),
            ('nøkrum', 'PBFPD'),
            ('nøkrum', 'PBMPD'),
            ('nøkrum', 'PBNPD'),
            ('nøkrum', 'PBNSD'),
            ('nøkrum', 'PNSD'),
            ('nøkur', 'PBFSN'),
            ('nøkur', 'PBNPA'),
            ('nøkur', 'PBNSA'),
            ('okkara', 'PP1PA'),
            ('okkara', 'PP1PD'),
            ('okkara', 'PP1PN'),
            ('okkum', 'PP1PA'),
            ('okkum', 'PP1PD'),
            ('onga', 'PBFSA'),
            ('ongan', 'PBMSA'),
            ('ongar', 'PBFPA'),
            ('ongar', 'PBMPA'),
            ('ongi', 'PBNPN'),
            ('ongin', 'PBNSN'),
            ('ongum', 'PBFPD'),
            ('ongum', 'PBFSD'),
            ('ongum', 'PBMSD'),
            ('ongum', 'PBNSD'),
            ('onki', 'PBNSN'),
            ('onkra', 'PBFSA'),
            ('onkra', 'PBNSA'),
            ('onkran', 'PBMSA'),
            ('onkrar', 'PBFPA'),
            ('onkrar', 'PBFPN'),
            ('onkrar', 'PBMPA'),
            ('onkrari', 'PBFSD'),
            ('onkrum', 'PBFPD'),
            ('onkrum', 'PBMPD'),
            ('onkrum', 'PBMSD'),
            ('onkrum', 'PBNPD'),
            ('onkrum', 'PBNSD'),
            ('onkur', 'PBNPA'),
            ('onnur', 'PBNPA'),
            ('sama', 'PIFSN'),
            ('sama', 'PIMSA'),
            ('sama', 'PIMSD'),
            ('sama', 'PINSA'),
            ('sama', 'PINSD'),
            ('sama', 'PINSN'),
            ('sami', 'PIMSN'),
            ('seg', 'PPFPA'),
            ('seg', 'PPFSA'),
            ('seg', 'PPMPA'),
            ('seg', 'PPMSA'),
            ('seg', 'PPNPA'),
            ('seg', 'PPNPN'),
            ('seg', 'PPNSA'),
            ('seg', 'PPNSN'),
            ('sinnaðir', 'PMPN'),
            ('sjálv', 'PIFSN'),
            ('sjálv', 'PINPA'),
            ('sjálv', 'PINPN'),
            ('sjálva', 'PIFSA'),
            ('sjálvan', 'PIMSA'),
            ('sjálvar', 'PIFPA'),
            ('sjálvar', 'PIFPN'),
            ('sjálvari', 'PIFSD'),
            ('sjálvi', 'PINPA'),
            ('sjálvi', 'PINPN'),
            ('sjálvir', 'PIMPN'),
            ('sjálvir', 'PIMSN'),
            ('sjálvt', 'PINSN'),
            ('sjálvum', 'PIMPD'),
            ('sjálvum', 'PIMSD'),
            ('sjálvum', 'PINPD'),
            ('sjálvum', 'PINSD'),
            ('sjálvur', 'PIMSN'),
            ('slík', 'PIFSN'),
            ('slík', 'PINPA'),
            ('slík', 'PINPN'),
            ('slíka', 'PIFSA'),
            ('slíkan', 'PIMSA'),
            ('slíkar', 'PIFPA'),
            ('slíkar', 'PIFPN'),
            ('slíkar', 'PIMPA'),
            ('slíkari', 'PIFSD'),
            ('slíkir', 'PIMPN'),
            ('slíkt', 'PINSA'),
            ('slíkt', 'PINSN'),
            ('slíkum', 'PIFPD'),
            ('slíkum', 'PIMPD'),
            ('slíkum', 'PIMSD'),
            ('slíkum', 'PINPD'),
            ('slíkum', 'PINSD'),
            ('slíkur', 'PIMSN'),
            ('somu', 'PIFPN'),
            ('somu', 'PIFSA'),
            ('somu', 'PIFSD'),
            ('somu', 'PIMPA'),
            ('somu', 'PIMPN'),
            ('somu', 'PINPD'),
            ('somu', 'PINPN'),
            ('summum', 'PBMSD'),
            ('sær', 'PPFPD'),
            ('sær', 'PPFPN'),
            ('sær', 'PPFSD'),
            ('sær', 'PPMPD'),
            ('sær', 'PPMSD'),
            ('sær', 'PPNPA'),
            ('sær', 'PPNPD'),
            ('sær', 'PPNSD'),
            ('sín', 'PPMSA'),
            ('sín', 'PPMSG'),
            ('sín', 'PPNPA'),
            ('sín', 'PPNSN'),
            ('sína', 'PPFSA'),
            ('sína', 'PPFSG'),
            ('sína', 'PPMSA'),
            ('sína', 'PPNSA'),
            ('sínar', 'PPFPA'),
            ('sínar', 'PPFPG'),
            ('sínar', 'PPMPA'),
            ('sínar', 'PPMSA'),
            ('sínar', 'PPMSG'),
            ('sínar', 'PPNPA'),
            ('sínari', 'PPFSD'),
            ('sínari', 'PPNSD'),
            ('síni', 'PPMPG'),
            ('síni', 'PPMSD'),
            ('síni', 'PPMSG'),
            ('síni', 'PPNPA'),
            ('síni', 'PPNPG'),
            ('síni', 'PPNPN'),
            ('síni', 'PPNSG'),
            ('sínum', 'PPFPD'),
            ('sínum', 'PPMPD'),
            ('sínum', 'PPMSD'),
            ('sínum', 'PPNPD'),
            ('sínum', 'PPNSD'),
            ('sítt', 'PEMPA'),
            ('sítt', 'PEMSA'),
            ('sítt', 'PENSA'),
            ('sítt', 'PENSG'),
            ('tann', 'PDFSA'),
            ('tað', 'PBNSN'),
            ('tað', 'PDFSA'),
            ('tað', 'PDNSA'),
            ('tað', 'PPNPN'),
            ('tað', 'PPNSA'),
            ('tað', 'PPNSN'),
            ('teg', 'PP2SA'),
            ('teim', 'PDFPD'),
            ('teim', 'PDMPD'),
            ('teim', 'PDNPD'),
            ('teimum', 'PBNPD'),
            ('teimum', 'PDFPD'),
            ('teimum', 'PDFSD'),
            ('teimum', 'PDMPD'),
            ('teimum', 'PDMSD'),
            ('teimum', 'PDNPD'),
            ('teimum', 'PDNSD'),
            ('teimum', 'PPFPD'),
            ('teimum', 'PPMPD'),
            ('teimum', 'PPNPD'),
            ('teir', 'PDMPA'),
            ('teir', 'PDNPN'),
            ('teir', 'PPMPA'),
            ('teir', 'PPMPN'),
            ('teir', 'PPNPN'),
            ('teirra', 'PPFPG'),
            ('teirra', 'PPMPG'),
            ('teirra', 'PPNPG'),
            ('teirri', 'PDFSD'),
            ('tess', 'PPNSG'),
            ('tey', 'PPNPA'),
            ('tey', 'PPNPN'),
            ('truplum', 'PBFPD'),
            ('tykkara', 'PP2PG'),
            ('tær', 'PDFPA'),
            ('tær', 'PDFSN'),
            ('tær', 'PDNPA'),
            ('tær', 'PP2SD'),
            ('tær', 'PPFPA'),
            ('tær', 'PPFPN'),
            ('tær', 'PPFSA'),
            ('tí', 'PDFSD'),
            ('tí', 'PDMSD'),
            ('tí', 'PDNSD'),
            ('tí', 'PPNSD'),
            ('tílík', 'PIFSN'),
            ('tílík', 'PINSN'),
            ('tílíkt', 'PINSA'),
            ('tílíkt', 'PINSN'),
            ('tín', 'PP2SG'),
            ('tína', 'PP2SG'),
            ('tínar', 'PPMPA'),
            ('vakrar', 'PBMPA'),
            ('øll', 'PBFSN'),
            ('øll', 'PBNPA'),
            ('øll', 'PBNPN'),
            ('øll', 'PNPN'),
            ('øllum', 'PBFPD'),
            ('øllum', 'PBMPD'),
            ('øllum', 'PBMSD'),
            ('øllum', 'PBNPA'),
            ('øllum', 'PBNPD'),
            ('øllum', 'PBNSD'),
            ('øðrum', 'PBFPD'),
            ('øðrum', 'PBMPD'),
            ('øðrum', 'PBMSD'),
            ('øðrum', 'PBNPD'),
            ('øðrum', 'PBNSD')]

for i in FN_PAIRS:
    print(i)

pairdict = defaultdict(list)

for pair in FN_PAIRS:
    pairdict[pair[1]].append(pair[0])
    
for k,v in pairdict.items():
    print(k+'\t'+'\t'.join(v) )
    