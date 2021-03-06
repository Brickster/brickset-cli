import unittest

from parameterized import parameterized

from bin import api

class TestApi(unittest.TestCase):

    def test_executeApiRequest(self):
        self.fail()

    def test_downloadInstruction(self):
        self.fail()

    @parameterized.expand([
        ['noDescription0', '{No longer listed at LEGO.com}', '1234-1_5678.pdf'],
        ['regionBookOfBooks0', 'BI 3017 / 32 - 70704 V39 2/2', '1234-1_v39_b2_5678.pdf'],
        ['regionBookOfBooks1', 'BI 3017 / 56 - 65g-70708 V39 1/2', '1234-1_v39_b1_5678.pdf'],
        ['regionBookOfBooks2', 'BI 3017 / 48 - 65g, 9525 V39  1/2', '1234-1_v39_b1_5678.pdf'],
        ['regionBookOfBooks3', 'BI 3017 / 48 - 65g, 9525 V29 1/2', '1234-1_v29_b1_5678.pdf'],
        ['regionBookOfBooks4', 'BI 3017 / 80+4 - 70704 V39 1/2', '1234-1_v39_b1_5678.pdf'],
        ['regionBookOfBooks5', 'BI 3016 80+4*- 10228 V29/39 1/3', '1234-1_v29_v39_b1_5678.pdf'],
        ['regionBookOfBooks6', 'BI 3101, 32/65G, 60257 V.39 4/4', '1234-1_v39_b4_5678.pdf'],
        ['regionBookOfBooks7', 'BI 3100, 64+4/65+115G, 60257 V.39 2/4', '1234-1_v39_b2_5678.pdf'],
        ['regionBookOfBooks8', 'BI 3103, 112+4/65+200G, 10270 V29 1/2', '1234-1_v29_b1_5678.pdf'],
        ['regionBookOfBooks9', 'BI 3103, 96+4/65+200G, V39/142 2/2', '1234-1_v39_v142_b2_5678.pdf'],
        ['regionBookOfBooks10', 'BI 3103, 96+4/65+200G,10270 V29 2/2', '1234-1_v29_b2_5678.pdf'],
        ['regionBookOfBooks11', 'BI 3003/24 - 21106 V. 29 2/2', '1234-1_v29_b2_5678.pdf'],
        ['regionBookOfBooks12', 'BI 3006/48 - 8096 V.29 2/2', '1234-1_v29_b2_5678.pdf'],
        ['regionBookOfBooks13', 'BI 3004/40 - 9498 V29 1/2', '1234-1_v29_b1_5678.pdf'],
        ['regionBookOfBooks14', 'BI 3006/56 - 10211 V46/39 1/3', '1234-1_v46_v39_b1_5678.pdf'],
        ['regionBookOfBooks15', 'BI 3003/24 -21107  V39 2/2', '1234-1_v39_b2_5678.pdf'],
        ['regionBookOfBooks16', 'BI 3003/32- 21107 V.39 1/2', '1234-1_v39_b1_5678.pdf'],
        ['regionBookOfBooks17', 'BI 3003/32-21105 V. 29 1/2', '1234-1_v29_b1_5678.pdf'],
        ['regionBookOfBooks18', 'BI 3003/32-21105 V.29 2/2', '1234-1_v29_b2_5678.pdf'],
        ['regionBookOfBooks19', 'BI 3009/48-65g 7961V29/39 1/2', '1234-1_v29_v39_b1_5678.pdf'],
        ['regionBookOfBooks20', 'BI 3019/40-65G-75025 V39 2/2', '1234-1_v39_b2_5678.pdf'],
        ['regionBookOfBooks21', 'BI 3019/44-65G-9525 V29/39 2/2', '1234-1_v29_v39_b2_5678.pdf'],
        ['regionBookOfBooks22', 'BI 3019/44-65G-9525 V29/39 BOOK2', '1234-1_v29_v39_b2_5678.pdf'],
        ['regionBookOfBooks23', 'BI 3009/48-65g7961V29/39 1/2', '1234-1_v29_v39_b1_5678.pdf'],
        ['regionBookOfBooks24', 'BI 3004/24, 10254 V39 1/2', '1234-1_v39_b1_5678.pdf'],
        ['regionBookOfBooks25', 'BI 3006/72+4 - 8096 V.29 1/2', '1234-1_v29_b1_5678.pdf'],
        ['regionBookOfBooks26', 'BI 3009/80+4 - 10220 V110  1 / 2', '1234-1_v110_b1_5678.pdf'],
        ['regionBookOfBooks27', 'BI 3009/80+4 - 10220 V140 2 / 2', '1234-1_v140_b2_5678.pdf'],
        ['regionBookOfBooks28', 'BI 3009/80+4 -10220 V46/39 2/2', '1234-1_v46_v39_b2_5678.pdf'],
        ['regionBookOfBooks29', 'BI 3009/76+4 7965 V 39 2/2', '1234-1_v39_b2_5678.pdf'],
        ['regionBookOfBooks30', 'BI 3009/80+4 7965 V 29/39 1/2', '1234-1_v29_v39_b1_5678.pdf'],
        ['regionBookOfBooks31', 'BI 3016/64+4-10228 V29/39 3/3', '1234-1_v29_v39_b3_5678.pdf'],
        ['regionBookOfBooks32', 'BI 3009/40+4-65g 7961 V39 2/2', '1234-1_v39_b2_5678.pdf'],
        ['regionBookOfBooks33', 'BI 3019/80+4*- 75025 V39 1/2', '1234-1_v39_b1_5678.pdf'],
        ['regionBookOfBooks34', 'BI 3006/64+4*- 10229 V29/39 2/2', '1234-1_v29_v39_b2_5678.pdf'],
        ['bookOfBooksRegion0', 'BI 3004 / 60+4 / 65+115g, 60227 3/4 V29', '1234-1_v29_b3_5678.pdf'],
        ['bookOfBooksRegion1', 'BI 3016 60/65g, 10243 3/3 V29', '1234-1_v29_b3_5678.pdf'],
        ['bookOfBooksRegion2', 'BI 3102, 40, 75317 1/2 V39', '1234-1_v39_b1_5678.pdf'],
        ['bookOfBooksRegion3', 'BI 3102, 48/65G, 75317 2/2 V39', '1234-1_v39_b2_5678.pdf'],
        ['bookOfBooksRegion4', 'BI 3019, 24/65G, 60227 4/4 V39/V142', '1234-1_v39_v142_b4_5678.pdf'],
        ['bookOfBooksRegion5', 'BI 3018, 80+4 - 31079 1/3 V39', '1234-1_v39_b1_5678.pdf'],
        ['bookOfBooksRegion6', 'BI 3106, 72+4/65+115G, 76899 2/2 V39', '1234-1_v39_b2_5678.pdf'],
        ['bookOfBooksRegion7', 'BI 3004,60+4,65+115,60227 3/4 V39/V142', '1234-1_v39_v142_b3_5678.pdf'],
        ['bookOfBooksRegion8', 'BI 3004/48 - 31079 3/3 V39', '1234-1_v39_b3_5678.pdf'],
        ['bookOfBooksRegion9', 'BI 3004/52 - 76003 BOOK 2/2 V39', '1234-1_v39_b2_5678.pdf'],
        ['bookOfBooksRegion10', 'BI 3017/48 - 65G, 10259 1/2 V39', '1234-1_v39_b1_5678.pdf'],
        ['bookOfBooksRegion11', 'BI 3016/56 10242 2/2 V39', '1234-1_v39_b2_5678.pdf'],
        ['bookOfBooksRegion12', 'BI 3016/36-65G 10245 1/2 V39', '1234-1_v39_b1_5678.pdf'],
        ['bookOfBooksRegion13', 'BI 3016/48-65G, 10243 2/3 V29', '1234-1_v29_b2_5678.pdf'],
        ['bookOfBooksRegion14', 'BI 3101/36, 75940 1/2 V39', '1234-1_v39_b1_5678.pdf'],
        ['bookOfBooksRegion15', 'BI 3004/40, 60227 1/4 V39/V142', '1234-1_v39_v142_b1_5678.pdf'],
        ['bookOfBooksRegion16', 'BI 3016/64+4 10242 1/2 V39', '1234-1_v39_b1_5678.pdf'],
        ['bookOfBooksRegion17', 'BI 3004/64+4-65, 75888 2/2 V39', '1234-1_v39_b2_5678.pdf'],
        ['bookOfBooksRegion18', 'BI 3106/72+4, 75940 2/2 V39', '1234-1_v39_b2_5678.pdf'],
        ['bookOfBooksRegion19', 'BI 3019/72+4*- 70709 1/2 v.39', '1234-1_v39_b1_5678.pdf'],
        ['bookOfBooksRegion20', 'BI 3002/68+4*- 79105 BOOK 2/2 V39', '1234-1_v39_b2_5678.pdf'],
        ['bookOfBooksRegion21', 'BI 3016/60+4*-, 10259 2/2 V39', '1234-1_v39_b2_5678.pdf'],
        ['bookOfBooksRegion22', 'BI 3016/68+4*, 10243 1/3 V39', '1234-1_v39_b1_5678.pdf'],
        ['bookOfBooksRegion23', 'BI 3016/68+4*,10243 1/3 V29', '1234-1_v29_b1_5678.pdf'],
        ['bookOfBooksRegion24', 'BI 3016/64+4/65+115g - 10245 2/2 V39', '1234-1_v39_b2_5678.pdf'],
        ['bookOfBooksRegion25', 'BI 3017/124+4/65+200G, 70831 2/2 V39', '1234-1_v39_b2_5678.pdf'],
        ['onlyBook1', 'BI 8557/1', '1234-1_b1_5678.pdf'],
        ['onlyBook0', 'BUILDING INSTRUCTION 8557/1', '1234-1_b1_5678.pdf'],
        ['onlyRegion0', 'BI 3017 / 60 - 70702 V39', '1234-1_v39_5678.pdf'],
        ['onlyRegion1', 'BI 3017 / 24 - 65g - 10525 V39', '1234-1_v39_5678.pdf'],
        ['onlyRegion2', 'BI 3017 / 76+4 - 70703 V39', '1234-1_v39_5678.pdf'],
        ['onlyRegion3', 'BI 3017 / 76+4 - 65/115g, 75101 V140', '1234-1_v140_5678.pdf'],
        ['onlyRegion4', 'BI 3019 / 304+4 / 65+200g, 10255 V29', '1234-1_v29_5678.pdf'],
        ['onlyRegion5', 'BI 9005 / 60x50 leaflet, 30525 V39', '1234-1_v39_5678.pdf'],
        ['onlyRegion6', 'BI 3004 60/ - 75003 V39', '1234-1_v39_5678.pdf'],
        ['onlyRegion7', 'BI 3016 80+4*-  79104 V110', '1234-1_v110_5678.pdf'],
        ['onlyRegion8', 'BI 3016 80+4*- 10222 V/39/46/110', '1234-1_v39_v46_v110_5678.pdf'],
        ['onlyRegion9', 'BI 3016 80+4*- 10222 V39/46/110', '1234-1_v39_v46_v110_5678.pdf'],
        ['onlyRegion10', 'BI 3107, 44/65G, 40436 V39', '1234-1_v39_5678.pdf'],
        ['onlyRegion11', 'BI 3105, 108+4, 40411 V39', '1234-1_v39_5678.pdf'],
        ['onlyRegion12', 'BI 3104, 244+4, 75292 V29/V118', '1234-1_v29_v118_5678.pdf'],
        ['onlyRegion13', 'BI 3004, 88+4, 65/200G, 70827 V39', '1234-1_v39_5678.pdf'],
        ['onlyRegion14', 'BI 3019, 160+4/65+200G, 21315 V.39', '1234-1_v39_5678.pdf'],
        ['onlyRegion15', 'BI 3106, 80+4/65+115G, 75958 V39', '1234-1_v39_5678.pdf'],
        ['onlyRegion16', 'BI 3019, 204+4/65+200G, 75212 V39 & V142', '1234-1_v39_v142_5678.pdf'],
        ['onlyRegion17', 'BI 3104, 100+4/65+200G, 75272 V39/V142', '1234-1_v39_v142_5678.pdf'],
        ['onlyRegion18', 'BI 2002/ 2 - 40109 V46', '1234-1_v46_5678.pdf'],
        ['onlyRegion19', 'BI 2001/ 2 -30265 V29', '1234-1_v29_5678.pdf'],
        ['onlyRegion20', 'BI 2002/ 2, 30620 V29', '1234-1_v29_5678.pdf'],
        ['onlyRegion21', 'BI 3003/24 - 3848 IN', '1234-1_in_5678.pdf'],
        ['onlyRegion22', 'BI 3001/16 - 7595 V 29', '1234-1_v29_5678.pdf'],
        ['onlyRegion23', 'BI 3004/56 - 7959 V 29/39', '1234-1_v29_v39_5678.pdf'],
        ['onlyRegion24', 'BI 3003/24 - 3848 V.92', '1234-1_v92_5678.pdf'],
        ['onlyRegion25', 'BI 3004/48 - 70706 V39', '1234-1_v39_5678.pdf'],
        ['onlyRegion26', 'BI 3001/16 - 7914 V29/39', '1234-1_v29_v39_5678.pdf'],
        ['onlyRegion27', 'BI 3004/24 -3858 IN', '1234-1_in_5678.pdf'],
        ['onlyRegion28', 'BI 3001/12 -71257 V110', '1234-1_v110_5678.pdf'],
        ['onlyRegion29', 'BI 3003/36-, 75197 V39', '1234-1_v39_5678.pdf'],
        ['onlyRegion30', 'BI 3022/12-65G -  COMIC BOOK 76003 V39', '1234-1_comic_v39_5678.pdf'],
        ['onlyRegion31', 'BI 3022/48-65G - 75085 V29', '1234-1_v29_5678.pdf'],
        ['onlyRegion32', 'BI 3018/60-65G -71253 V110', '1234-1_v110_5678.pdf'],
        ['onlyRegion33', 'BI 3018/60-65g, 71242 V39', '1234-1_v39_5678.pdf'],
        ['onlyRegion34', 'BI 3004/20, 3857 IN', '1234-1_in_5678.pdf'],
        ['onlyRegion35', 'BI 3016/56, 10242 V140', '1234-1_v140_5678.pdf'],
        ['onlyRegion36', 'BI 3005/72+4 - 7930 V 29/39', '1234-1_v29_v39_5678.pdf'],
        ['onlyRegion37', 'BI 3006/72+4 -10199 V46 + V110', '1234-1_v46_v110_5678.pdf'],
        ['onlyRegion38', 'BI 3009/64+4 7931 V 29/39', '1234-1_v29_v39_5678.pdf'],
        ['onlyRegion39', 'BI 3006/80+4 10216 V46/110/39', '1234-1_v46_v110_v39_5678.pdf'],
        ['onlyRegion40', 'BI 3004/60+4-75048 V29', '1234-1_v29_5678.pdf'],
        ['onlyRegion41', 'BI 3016/72+4-9526 V29/39', '1234-1_v29_v39_5678.pdf'],
        ['onlyRegion42', 'BI 3022/72+4-65+115G, 70901 V39', '1234-1_v39_5678.pdf'],
        ['onlyRegion43', 'BI 3004/80+4, 76102 V39', '1234-1_v39_5678.pdf'],
        ['onlyRegion44', 'BI 3004/68+4*- 9494 V 29/39', '1234-1_v29_v39_5678.pdf'],
        ['onlyRegion45', 'BI 3016/76+4*- 79104 V29', '1234-1_v29_5678.pdf'],
        ['onlyRegion46', 'BI 3019/80+4*, 75179 V39', '1234-1_v39_5678.pdf'],
        ['onlyRegion47', 'BI 3016/172+4/65+200g , 10246 V39', '1234-1_v39_5678.pdf'],
        ['onlyRegion48', 'BI 3004/84+4/115+150g 21109 V.46', '1234-1_v46_5678.pdf'],
        ['onlyRegion49', 'BI 3004/104+4/115+350g- 21103 V29', '1234-1_v29_5678.pdf'],
        ['onlyRegion50', 'BI 3004/108+4/115+350g-21103 V39', '1234-1_v39_5678.pdf'],
        ['onlyRegion51', 'BI 3019/148+4/65+200G, 21315 V.29', '1234-1_v29_5678.pdf'],
        ['onlyRegion52', 'BI 3019/92+4/65+200G, 70820 V39', '1234-1_v39_5678.pdf'],
        ['bookOfBooks0', 'BI 3006/56 - 8019 1/2', '1234-1_b1_5678.pdf'],
        ['buildingInstructions0', 'BI 1433', '1234-1_5678.pdf'],
        ['buildingInstructions1', 'BI 3002/24 - 3838', '1234-1_5678.pdf'],
        ['buildingInstructions2', 'BI 3004/24 -3874', '1234-1_5678.pdf'],
        ['buildingInstructions3', 'BI 3004/80+4 7751', '1234-1_5678.pdf'],
        ['buildingInstructions4', 'BUILDING INSTRUCTION  8540', '1234-1_5678.pdf'],
        ['buildingInstructions5', 'BUILDING INSTRUCTION 7661', '1234-1_5678.pdf'],
        ['buildingInstructions6', 'BUILDING INSTRUCTION, 7256', '1234-1_5678.pdf'],
        ['buildingInstructions7', 'BUILDINGINSTRUCTION 8535', '1234-1_5678.pdf'],
        ['buildingInstructions8', 'BULDING INSTRUCTION, 8593', '1234-1_5678.pdf'],
        ['buildingInstructions9', 'BULDINGINSTRUCTION, 8596', '1234-1_5678.pdf']
    ])
    def test__constructInstructionFilename(self, name, instruction_description, expected):
        self.assertEquals(api._construct_instruction_filename('1234-1', instruction_description, 'https://www.lego.com/cdn/5678.pdf'), expected)

    def test__cleanRegion(self):
        self.fail()
