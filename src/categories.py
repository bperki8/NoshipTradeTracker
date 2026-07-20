"""Maps HS (Harmonized System) code chapters to product categories.

HS codes are 6-10 digit international commodity codes. The first 2 digits
(the chapter) broadly identify the product type. This module maps those
chapters to our simplified product categories for analysis.

https://hts.usitc.gov/
"""

from .models import ProductCategory, ProductType, WeaponizabilityLikelihood

# HS chapter (first 2 digits) to ProductCategory mapping.
# See Table of Contents here: https://hts.usitc.gov/
# TODO: Update the description and lists in the README.
HS_CHAPTER_TO_TYPE: dict[str, ProductType] = {
  # Section I LIVE ANIMALS; ANIMAL PRODUCTS
  "01": ProductType(ProductCategory.ANIMALS, WeaponizabilityLikelihood.LOWEST),  # Live animals
  "02": ProductType(ProductCategory.ANIMALS, WeaponizabilityLikelihood.LOWEST),  # Meat and edible meat offal
  "03": ProductType(ProductCategory.ANIMALS, WeaponizabilityLikelihood.LOWEST),  # Fish and crustaceans, molluscs and other aquatic invertebrates
  "04": ProductType(ProductCategory.ANIMALS, WeaponizabilityLikelihood.LOWEST),  # Dairy produce; birds´ eggs; natural honey; edible products of animal origin, not elsewhere specified or included
  "05": ProductType(ProductCategory.ANIMALS, WeaponizabilityLikelihood.LOWEST),  # Products of animal origin, not elsewhere specified or included
  # Section II VEGETABLE PRODUCTS
  "06": ProductType(ProductCategory.PLANTS, WeaponizabilityLikelihood.LOWEST),   # Live trees and other plants; bulbs, roots and the like; cut flowers and ornamental foliage
  "07": ProductType(ProductCategory.PLANTS, WeaponizabilityLikelihood.LOWEST),   # Edible vegetables and certain roots and tubers
  "08": ProductType(ProductCategory.PLANTS, WeaponizabilityLikelihood.LOWEST),   # Edible fruit and nuts; peel of citrus fruit or melons
  "09": ProductType(ProductCategory.PLANTS, WeaponizabilityLikelihood.LOWEST),   # Coffee, tea, maté and spices
  "10": ProductType(ProductCategory.PLANTS, WeaponizabilityLikelihood.LOWEST),   # Cereals
  "11": ProductType(ProductCategory.PLANTS, WeaponizabilityLikelihood.LOWEST),   # Products of the milling industry; malt; starches; inulin; wheat gluten
  "12": ProductType(ProductCategory.PLANTS, WeaponizabilityLikelihood.LOWEST),   # Oil seeds and oleaginous fruits; miscellaneous grains, seeds and fruit; industrial or medicinal plants; straw and fodder
  "13": ProductType(ProductCategory.PLANTS, WeaponizabilityLikelihood.LOWEST),   # Lac; gums; resins and other vegetable saps and extracts
  "14": ProductType(ProductCategory.PLANTS, WeaponizabilityLikelihood.LOWEST),   # Vegetable plaiting materials; vegetable products not elsewhere specified or included
  # SECTION III ANIMAL, VEGETABLE OR MICROBIAL FATS AND OILS AND THEIR CLEAVAGE PRODUCTS; PREPARED EDIBLE FATS; ANIMAL OR VEGETABLE WAXES
  "15": ProductType(ProductCategory.ANIMALS, WeaponizabilityLikelihood.LOWEST),   # Animal, vegetable or microbial fats and oils and their cleavage products; prepared edible fats; animal or vegetable waxes
  # SECTION IV PREPARED FOODSTUFFS; BEVERAGES, SPIRITS AND VINEGAR; TOBACCO AND MANUFACTURED TOBACCO SUBSTITUTES; PRODUCTS, WHETHER OR NOT CONTAINING NICOTINE, INTENDED FOR INHALATION WITHOUT COMBUSTION; OTHER NICOTINE CONTAINING PRODUCTS INTENDED FOR THE INTAKE OF NICOTINE INTO THE HUMAN BODY
  "16": ProductType(ProductCategory.ANIMALS, WeaponizabilityLikelihood.LOWEST),  # Preparations of meat, of fish, of crustaceans, molluscs or other aquatic invertebrates, or of insects
  "17": ProductType(ProductCategory.PLANTS, WeaponizabilityLikelihood.LOWEST),   # Sugars and sugar confectionery
  "18": ProductType(ProductCategory.PLANTS, WeaponizabilityLikelihood.LOWEST),   # Cocoa and cocoa preparations
  "19": ProductType(ProductCategory.PLANTS, WeaponizabilityLikelihood.LOWEST),   # Preparations of cereals, flour, starch or milk; bakers' wares
  "20": ProductType(ProductCategory.PLANTS, WeaponizabilityLikelihood.LOWEST),   # Preparations of vegetables, fruit, nuts or other parts of plants
  "21": ProductType(ProductCategory.ANIMALS, WeaponizabilityLikelihood.LOWEST),   # Miscellaneous edible preparations
  "22": ProductType(ProductCategory.PLANTS, WeaponizabilityLikelihood.LOWEST),   # Beverages, spirits and vinegar
  "23": ProductType(ProductCategory.ANIMALS, WeaponizabilityLikelihood.LOWEST),  # Residues and waste from the food industries; prepared animal feed
  "24": ProductType(ProductCategory.PLANTS, WeaponizabilityLikelihood.LOWEST),   # Tobacco and manufactured tobacco substitutes; products whether or not containing nicotine, intended for inhalation without combustion; other nicotine containing products intended for the intake of nicotine into the human body
  # SECTION V MINERAL PRODUCTS
  "25": ProductType(ProductCategory.MINERALS, WeaponizabilityLikelihood.LOWEST), # Salt; sulfur; earths and stone; plastering materials, lime and cement
  "26": ProductType(ProductCategory.MINERALS, WeaponizabilityLikelihood.LOWEST), # Ores, slag, ash
  "27": ProductType(ProductCategory.MINERALS, WeaponizabilityLikelihood.LOWEST), # Mineral fuels, mineral oils and products of their distillation; bituminous substances; mineral waxes
  # SECTION VI PRODUCTS OF THE CHEMICAL OR ALLIED INDUSTRIES
  "28": ProductType(ProductCategory.CHEMICALS, WeaponizabilityLikelihood.LOWEST),  # Inorganic chemicals; organic or inorganic compounds of precious metals, of rare-earth metals, of radioactive elements or of isotopes
  "29": ProductType(ProductCategory.CHEMICALS, WeaponizabilityLikelihood.LOWEST),  # Organic chemicals
  "30": ProductType(ProductCategory.HEALTH, WeaponizabilityLikelihood.LOWEST),     # Pharmaceutical products
  "31": ProductType(ProductCategory.CHEMICALS, WeaponizabilityLikelihood.LOWEST),  # Fertilizers
  "32": ProductType(ProductCategory.CHEMICALS, WeaponizabilityLikelihood.LOWEST),  # Tanning or dyeing extracts; tannins and their derivatives; dyes, pigments and other coloring matter; paints and varnishes; putty and other mastics; inks
  "33": ProductType(ProductCategory.CHEMICALS, WeaponizabilityLikelihood.LOWEST),     # Essential oils and resinoids; perfumery, cosmetic or toilet preparations
  "34": ProductType(ProductCategory.CHEMICALS, WeaponizabilityLikelihood.LOWEST),  # Soap, organic surface-active agents, washing preparations, lubricating preparations, artificial waxes, prepared waxes, polishing or scouring preparations, candles and similar articles, modeling pastes,"dental waxes" and dental preparations with a basis of plaster
  "35": ProductType(ProductCategory.CHEMICALS, WeaponizabilityLikelihood.LOWEST),  # Albuminoidal substances; modified starches; glues; enzymes
  "36": ProductType(ProductCategory.CHEMICALS, WeaponizabilityLikelihood.HIGHEST),  # Explosives; pyrotechnic products; matches; pyrophoric alloys; certain combustible preparations
  "37": ProductType(ProductCategory.CHEMICALS, WeaponizabilityLikelihood.LOWEST),  # Photographic or cinematographic goods
  "38": ProductType(ProductCategory.CHEMICALS, WeaponizabilityLikelihood.LOWEST),  # Miscellaneous chemical products
  # SECTION VII PLASTICS AND ARTICLES THEREOF; RUBBER AND ARTICLES THEREOF
  # TODO: I think some of these in chapters 39 and 40 need a re-looking at.
  "39": ProductType(ProductCategory.PLASTICS_RUBBER, WeaponizabilityLikelihood.LOWEST), # Plastics and articles thereof
  "40": ProductType(ProductCategory.PLASTICS_RUBBER, WeaponizabilityLikelihood.LOWEST), # Rubber and articles thereof
  # SECTION VIII RAW HIDES AND SKINS, LEATHER, FURSKINS AND ARTICLES THEREOF; SADDLERY AND HARNESS; TRAVEL GOODS, HANDBAGS AND SIMILAR CONTAINERS; ARTICLES OF ANIMAL GUT (OTHER THAN SILKWORM GUT)
  "41": ProductType(ProductCategory.ANIMALS, WeaponizabilityLikelihood.LOWEST),  # Raw hides and skins (other than furskins) and leather
  "42": ProductType(ProductCategory.ANIMALS, WeaponizabilityLikelihood.LOWEST),  # Articles of leather; saddlery and harness; travel goods, handbags and similar containers; articles of animal gut (other than silkworm gut)
  "43": ProductType(ProductCategory.ANIMALS, WeaponizabilityLikelihood.LOWEST),  # Furskins and artificial fur; manufactures thereof
  # SECTION IX WOOD AND ARTICLES OF WOOD;WOOD CHARCOAL; CORK AND ARTICLES OF CORK; MANUFACTURES OF STRAW, OF ESPARTO OR OF OTHER PLAITING MATERIALS; BASKETWARE AND WICKERWORK
  "44": ProductType(ProductCategory.WOOD_PAPER, WeaponizabilityLikelihood.LOWEST), # Wood and articles of wood; wood charcoal
  "45": ProductType(ProductCategory.WOOD_PAPER, WeaponizabilityLikelihood.LOWEST), # Cork and articles of cork
  "46": ProductType(ProductCategory.WOOD_PAPER, WeaponizabilityLikelihood.LOWEST), # Manufactures of straw, of esparto or of other plaiting materials; basketware and wickerwork
  # SECTION X PULP OF WOOD OR OF OTHER FIBROUS CELLULOSIC MATERIAL; RECOVERED (WASTE AND SCRAP) PAPER OR PAPERBOARD; PAPER AND PAPERBOARD AND ARTICLES THEREOF
  "47": ProductType(ProductCategory.WOOD_PAPER, WeaponizabilityLikelihood.LOWEST), # Pulp of wood or of other fibrous cellulosic material; recovered (waste and scrap) paper or paperboard
  "48": ProductType(ProductCategory.WOOD_PAPER, WeaponizabilityLikelihood.LOWEST), # Paper and paperboard; articles of paper pulp, of paper or of paperboard
  "49": ProductType(ProductCategory.WOOD_PAPER, WeaponizabilityLikelihood.LOWEST), # Printed books, newspapers, pictures and other products of the printing industry; manuscripts, typescripts and plans
  # SECTION XI TEXTILES AND TEXTILE ARTICLES
  # TODO: Potentially undercounting animal exploitation in this section. (There were some dairy machines in the machinery section, too. Would need to count those.)
  "50": ProductType(ProductCategory.ANIMALS, WeaponizabilityLikelihood.LOWEST),  # Silk
  "51": ProductType(ProductCategory.ANIMALS, WeaponizabilityLikelihood.LOWEST),  # Wool, fine or coarse animal hair; horsehair yarn and woven fabric
  "52": ProductType(ProductCategory.TEXTILES, WeaponizabilityLikelihood.LOWEST), # Cotton
  "53": ProductType(ProductCategory.TEXTILES, WeaponizabilityLikelihood.LOWEST), # Other vegetable textile fibers; paper yarn and woven fabrics of paper yarn
  "54": ProductType(ProductCategory.TEXTILES, WeaponizabilityLikelihood.LOWEST), # Man-made filaments; strip and the like of man-made textile materials
  "55": ProductType(ProductCategory.TEXTILES, WeaponizabilityLikelihood.LOWEST), # Man-made staple fibers
  "56": ProductType(ProductCategory.TEXTILES, WeaponizabilityLikelihood.LOWEST), # Wadding, felt and nonwovens; special yarns; twine, cordage, ropes and cables and articles thereof
  "57": ProductType(ProductCategory.TEXTILES, WeaponizabilityLikelihood.LOWEST), # Carpets and other textile floor coverings
  "58": ProductType(ProductCategory.TEXTILES, WeaponizabilityLikelihood.LOWEST), # Special woven fabrics; tufted textile fabrics; lace; tapestries; trimmings; embroidery
  "59": ProductType(ProductCategory.TEXTILES, WeaponizabilityLikelihood.LOWEST), # Impregnated, coated, covered or laminated textile fabrics; textile articles of a kind suitable for industrial use
  "60": ProductType(ProductCategory.TEXTILES, WeaponizabilityLikelihood.LOWEST), # Knitted or crocheted fabrics
  "61": ProductType(ProductCategory.TEXTILES, WeaponizabilityLikelihood.LOWEST), # Articles of apparel and clothing accessories, knitted or crocheted
  "62": ProductType(ProductCategory.TEXTILES, WeaponizabilityLikelihood.LOWEST), # Articles of apparel and clothing accessories, not knitted or crocheted
  "63": ProductType(ProductCategory.TEXTILES, WeaponizabilityLikelihood.LOWEST), # Other made up textile articles; needlecraft sets; worn clothing and worn textile articles; rags
  # SECTION XII FOOTWEAR, HEADGEAR, UMBRELLAS, SUN UMBRELLAS, WALKING-STICKS, SEAT-STICKS, WHIPS, RIDING-CROPS AND PARTS THEREOF; PREPARED FEATHERS AND ARTICLES MADE THEREWITH; ARTIFICIAL FLOWERS; ARTICLES OF HUMAN HAIR
  "64": ProductType(ProductCategory.TEXTILES, WeaponizabilityLikelihood.LOWEST), # Footwear, gaiters and the like; parts of such articles
  "65": ProductType(ProductCategory.TEXTILES, WeaponizabilityLikelihood.LOWEST), # Headgear and parts thereof 
  "66": ProductType(ProductCategory.TEXTILES, WeaponizabilityLikelihood.LOWEST), # Umbrellas, sun umbrellas, walking-sticks, seat-sticks, whips, riding-crops and parts thereof
  "67": ProductType(ProductCategory.ANIMALS, WeaponizabilityLikelihood.LOWEST), # Prepared feathers and down and articles made of feathers or of down; artificial flowers; articles of human hair
  # SECTION XIII ARTICLES OF STONE, PLASTER, CEMENT, ASBESTOS, MICA OR SIMILAR MATERIALS; CERAMIC PRODUCTS; GLASS AND GLASSWARE
  "68": ProductType(ProductCategory.STONE_CERAMIC_GLASS, WeaponizabilityLikelihood.LOWEST), # Articles of stone, plaster, cement, asbestos, mica or similar materials
  "69": ProductType(ProductCategory.STONE_CERAMIC_GLASS, WeaponizabilityLikelihood.LOWEST), # Ceramic products
  "70": ProductType(ProductCategory.STONE_CERAMIC_GLASS, WeaponizabilityLikelihood.LOWEST), # Glass and glassware
  # SECTION XIV NATURAL OR CULTURED PEARLS, PRECIOUS OR SEMIPRECIOUS STONES, PRECIOUS METALS, METALS CLAD WITH PRECIOUS METAL, AND ARTICLES THEREOF; IMITATION JEWELRY; COIN
  "71": ProductType(ProductCategory.METALS, WeaponizabilityLikelihood.LOWEST), # Natural or cultured pearls, precious or semiprecious stones, precious metals, metals clad with precious metal, and articles thereof; imitation jewelry; coin
  # SECTION XV BASE METALS AND ARTICLES OF BASE METAL
  "72": ProductType(ProductCategory.METALS, WeaponizabilityLikelihood.LOWEST), # Iron and steel
  "73": ProductType(ProductCategory.METALS, WeaponizabilityLikelihood.LOW), # Articles of iron or steel
  "74": ProductType(ProductCategory.METALS, WeaponizabilityLikelihood.LOWEST), # Copper and articles thereof
  "75": ProductType(ProductCategory.METALS, WeaponizabilityLikelihood.LOWEST), # Nickel and articles thereof
  "76": ProductType(ProductCategory.METALS, WeaponizabilityLikelihood.LOWEST), # Aluminum and articles thereof
  # "77": (Reserved for possible future use)
  "78": ProductType(ProductCategory.METALS, WeaponizabilityLikelihood.LOWEST), # Lead and articles thereof
  "79": ProductType(ProductCategory.METALS, WeaponizabilityLikelihood.LOWEST), # Zinc and articles thereof
  "80": ProductType(ProductCategory.METALS, WeaponizabilityLikelihood.LOWEST), # Tin and articles thereof
  "81": ProductType(ProductCategory.METALS, WeaponizabilityLikelihood.LOWEST), # Other base metals; cermets; articles thereof
  "82": ProductType(ProductCategory.METALS, WeaponizabilityLikelihood.LOWEST), # Tools, implements, cutlery, spoons and forks, of base metal; parts thereof of base metal
  "83": ProductType(ProductCategory.METALS, WeaponizabilityLikelihood.LOWEST), # Miscellaneous articles of base metal
  # SECTION XVI MACHINERY AND MECHANICAL APPLIANCES; ELECTRICAL EQUIPMENT; PARTS THEREOF; SOUND RECORDERS AND REPRODUCERS, TELEVISION IMAGE AND SOUND RECORDERS AND REPRODUCERS, AND PARTS AND ACCESSORIES OF SUCH ARTICLES
  # TODO: Nuclear reactors!?!
  "84": ProductType(ProductCategory.MACHINERY, WeaponizabilityLikelihood.LOWEST), # Nuclear reactors, boilers, machinery and mechanical appliances; parts thereof
  "85": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.LOWEST), # Electrical machinery and equipment and parts thereof; sound recorders and reproducers, television image and sound recorders and reproducers, and parts and accessories of such articles
  # SECTION XVII VEHICLES, AIRCRAFT, VESSELS AND ASSOCIATED TRANSPORT EQUIPMENT
  "86": ProductType(ProductCategory.VEHICLES, WeaponizabilityLikelihood.LOW), # Railway or tramway locomotives, rolling stock and parts thereof; railway or tramway track fixtures and fittings and parts thereof; mechanical (including electro-mechanical) traffic signaling equipment of all kinds
  "87": ProductType(ProductCategory.VEHICLES, WeaponizabilityLikelihood.LOW), # Vehicles other than railway or tramway rolling stock, and parts and accessories thereof
  "88": ProductType(ProductCategory.VEHICLES, WeaponizabilityLikelihood.HIGH), # Aircraft, spacecraft, and parts thereof
  "89": ProductType(ProductCategory.VEHICLES, WeaponizabilityLikelihood.LOW), # Ships, boats and floating structures
  # SECTION XVIII OPTICAL, PHOTOGRAPHIC, CINEMATOGRAPHIC, MEASURING, CHECKING, PRECISION, MEDICAL OR SURGICAL INSTRUMENTS AND APPARATUS; CLOCKS AND WATCHES; MUSICAL INSTRUMENTS; PARTS AND ACCESSORIES THEREOF
  "90": ProductType(ProductCategory.INSTRUMENTS, WeaponizabilityLikelihood.LOWEST), # Optical, photographic, cinematographic, measuring, checking, precision, medical or surgical instruments and apparatus; parts and accessories thereof
  "91": ProductType(ProductCategory.INSTRUMENTS, WeaponizabilityLikelihood.LOWEST), # Clocks and watches and parts thereof
  "92": ProductType(ProductCategory.INSTRUMENTS, WeaponizabilityLikelihood.LOWEST), # Musical instruments; parts and accessories of such articles
  # SECTION XIX ARMS AND AMMUNITION; PARTS AND ACCESSORIES THEREOF
  "93": ProductType(ProductCategory.WEAPONS, WeaponizabilityLikelihood.HIGHEST), # Arms and ammunition; parts and accessories thereof
  # SECTION XX MISCELLANEOUS MANUFACTURED ARTICLES
  "94": ProductType(ProductCategory.MANUFACTURED, WeaponizabilityLikelihood.LOWEST), # Furniture; bedding, mattresses, mattress supports, cushions and similar stuffed furnishings; luminaires and lighting fittings, not elsewhere specified or included; illuminated signs, illuminated nameplates and the like; prefabricated buildings
  "95": ProductType(ProductCategory.MANUFACTURED, WeaponizabilityLikelihood.LOWEST), # Toys, games and sports equipment; parts and accessories thereof
  "96": ProductType(ProductCategory.MANUFACTURED, WeaponizabilityLikelihood.LOWEST), # Miscellaneous manufactured articles
  # SECTION XXI WORKS OF ART, COLLECTORS' PIECES AND ANTIQUES
  "97": ProductType(ProductCategory.ART, WeaponizabilityLikelihood.LOWEST), # Works of art, collectors' pieces and antiques
  # SECTION XXII SPECIAL CLASSIFICATION PROVISIONS; TEMPORARY LEGISLATION; TEMPORARY MODIFICATIONS ESTABLISHED PURSUANT TO TRADE LEGISLATION; ADDITIONAL IMPORT RESTRICTIONS ESTABLISHED PURSUANT TO SECTION 22 OF THE AGRICULTURAL ADJUSTMENT ACT, AS AMENDED
  "98": ProductType(ProductCategory.SPECIAL, WeaponizabilityLikelihood.LOW), # Special classification provisions
  "99": ProductType(ProductCategory.SPECIAL, WeaponizabilityLikelihood.LOWEST), # Temporary legislation; temporary modifications established pursuant to trade legislation; additional import restrictions established pursuant to section 22 of the Agricultural Adjustment Act, as amended
}

HS_CODE_OVERRIDES: dict[str, ProductType] = {
  "271019": ProductType(ProductCategory.MINERALS, WeaponizabilityLikelihood.LOW),
  "271311": ProductType(ProductCategory.MINERALS, WeaponizabilityLikelihood.LOW),
  "271312" : ProductType(ProductCategory.MINERALS, WeaponizabilityLikelihood.LOW),

  "280429": ProductType(ProductCategory.CHEMICALS, WeaponizabilityLikelihood.LOW),
  "280430": ProductType(ProductCategory.CHEMICALS, WeaponizabilityLikelihood.HIGH),
  "280461": ProductType(ProductCategory.CHEMICALS, WeaponizabilityLikelihood.HIGH),
  "280530": ProductType(ProductCategory.CHEMICALS, WeaponizabilityLikelihood.HIGH),
  "281122": ProductType(ProductCategory.CHEMICALS, WeaponizabilityLikelihood.HIGH),
  "281129": ProductType(ProductCategory.CHEMICALS, WeaponizabilityLikelihood.HIGH),
  "281219": ProductType(ProductCategory.CHEMICALS, WeaponizabilityLikelihood.HIGH),
  "281290": ProductType(ProductCategory.CHEMICALS, WeaponizabilityLikelihood.HIGH),
  "282540": ProductType(ProductCategory.CHEMICALS, WeaponizabilityLikelihood.HIGH),
  "282570": ProductType(ProductCategory.CHEMICALS, WeaponizabilityLikelihood.HIGH),
  "282590": ProductType(ProductCategory.CHEMICALS, WeaponizabilityLikelihood.LOW),
  "282619": ProductType(ProductCategory.CHEMICALS, WeaponizabilityLikelihood.HIGH),
  "282739": ProductType(ProductCategory.CHEMICALS, WeaponizabilityLikelihood.HIGH),
  "283090": ProductType(ProductCategory.CHEMICALS, WeaponizabilityLikelihood.HIGH),
  "283340": ProductType(ProductCategory.CHEMICALS, WeaponizabilityLikelihood.LOW),
  "283510": ProductType(ProductCategory.CHEMICALS, WeaponizabilityLikelihood.LOW),
  "283699": ProductType(ProductCategory.CHEMICALS, WeaponizabilityLikelihood.LOW),
  "284310": ProductType(ProductCategory.CHEMICALS, WeaponizabilityLikelihood.LOW),
  "284330": ProductType(ProductCategory.CHEMICALS, WeaponizabilityLikelihood.HIGH),
  "284390": ProductType(ProductCategory.CHEMICALS, WeaponizabilityLikelihood.HIGH),
  "284590": ProductType(ProductCategory.CHEMICALS, WeaponizabilityLikelihood.HIGH),
  "284990": ProductType(ProductCategory.CHEMICALS, WeaponizabilityLikelihood.HIGH),
  "285390": ProductType(ProductCategory.CHEMICALS, WeaponizabilityLikelihood.HIGH),

  "380110": ProductType(ProductCategory.CHEMICALS, WeaponizabilityLikelihood.HIGH),
  "381090": ProductType(ProductCategory.CHEMICALS, WeaponizabilityLikelihood.LOW),
  "381800": ProductType(ProductCategory.CHEMICALS, WeaponizabilityLikelihood.LOW),

  "391721": ProductType(ProductCategory.PLASTICS_RUBBER, WeaponizabilityLikelihood.HIGH),
  "391729": ProductType(ProductCategory.PLASTICS_RUBBER, WeaponizabilityLikelihood.HIGH),

  "401693": ProductType(ProductCategory.PLASTICS_RUBBER, WeaponizabilityLikelihood.HIGH),
  "401700": ProductType(ProductCategory.PLASTICS_RUBBER, WeaponizabilityLikelihood.HIGH),

  "420222": ProductType(ProductCategory.ANIMALS, WeaponizabilityLikelihood.LOW),
  "420330": ProductType(ProductCategory.ANIMALS, WeaponizabilityLikelihood.LOW),

  "591190": ProductType(ProductCategory.TEXTILES, WeaponizabilityLikelihood.LOW),

  "630533": ProductType(ProductCategory.TEXTILES, WeaponizabilityLikelihood.LOW),
  "630539": ProductType(ProductCategory.TEXTILES, WeaponizabilityLikelihood.LOW),
  "630622": ProductType(ProductCategory.TEXTILES, WeaponizabilityLikelihood.LOW),
  "630629": ProductType(ProductCategory.TEXTILES, WeaponizabilityLikelihood.LOW),
  "630690": ProductType(ProductCategory.TEXTILES, WeaponizabilityLikelihood.LOW),
  "630710": ProductType(ProductCategory.TEXTILES, WeaponizabilityLikelihood.LOW),
  "630720": ProductType(ProductCategory.TEXTILES, WeaponizabilityLikelihood.HIGH),

  "650610": ProductType(ProductCategory.TEXTILES, WeaponizabilityLikelihood.HIGH),
  "650691": ProductType(ProductCategory.TEXTILES, WeaponizabilityLikelihood.HIGH),
  "650700": ProductType(ProductCategory.TEXTILES, WeaponizabilityLikelihood.LOW),

  "680410": ProductType(ProductCategory.STONE_CERAMIC_GLASS, WeaponizabilityLikelihood.LOW),
  "680421": ProductType(ProductCategory.STONE_CERAMIC_GLASS, WeaponizabilityLikelihood.LOW),
  "680423": ProductType(ProductCategory.STONE_CERAMIC_GLASS, WeaponizabilityLikelihood.LOW),
  "680430": ProductType(ProductCategory.STONE_CERAMIC_GLASS, WeaponizabilityLikelihood.LOW),
  "681511": ProductType(ProductCategory.STONE_CERAMIC_GLASS, WeaponizabilityLikelihood.HIGH),
  "681513": ProductType(ProductCategory.STONE_CERAMIC_GLASS, WeaponizabilityLikelihood.HIGH),
  "681519": ProductType(ProductCategory.STONE_CERAMIC_GLASS, WeaponizabilityLikelihood.HIGH),

  "690390": ProductType(ProductCategory.STONE_CERAMIC_GLASS, WeaponizabilityLikelihood.LOW),
  "690911": ProductType(ProductCategory.STONE_CERAMIC_GLASS, WeaponizabilityLikelihood.LOW),
  "690919": ProductType(ProductCategory.STONE_CERAMIC_GLASS, WeaponizabilityLikelihood.HIGH),

  "701400": ProductType(ProductCategory.STONE_CERAMIC_GLASS, WeaponizabilityLikelihood.LOW),
  "701720": ProductType(ProductCategory.STONE_CERAMIC_GLASS, WeaponizabilityLikelihood.HIGH),

  "710229": ProductType(ProductCategory.METALS, WeaponizabilityLikelihood.LOW),
  "710510": ProductType(ProductCategory.METALS, WeaponizabilityLikelihood.LOW),
  "711019": ProductType(ProductCategory.METALS, WeaponizabilityLikelihood.HIGH),
  "711021": ProductType(ProductCategory.METALS, WeaponizabilityLikelihood.HIGH),

  "720221": ProductType(ProductCategory.METALS, WeaponizabilityLikelihood.LOW),
  "720521": ProductType(ProductCategory.METALS, WeaponizabilityLikelihood.LOW),
  "721790": ProductType(ProductCategory.METALS, WeaponizabilityLikelihood.LOW),

  "731029": ProductType(ProductCategory.METALS, WeaponizabilityLikelihood.HIGH),
  "731100": ProductType(ProductCategory.METALS, WeaponizabilityLikelihood.HIGH),
  "731210": ProductType(ProductCategory.METALS, WeaponizabilityLikelihood.HIGH),
  "731420": ProductType(ProductCategory.METALS, WeaponizabilityLikelihood.HIGH),
  "731582": ProductType(ProductCategory.METALS, WeaponizabilityLikelihood.HIGH),
  "731600": ProductType(ProductCategory.METALS, WeaponizabilityLikelihood.HIGH),
  "731812": ProductType(ProductCategory.METALS, WeaponizabilityLikelihood.LOWEST),
  "731813": ProductType(ProductCategory.METALS, WeaponizabilityLikelihood.LOWEST),
  "732393": ProductType(ProductCategory.METALS, WeaponizabilityLikelihood.LOWEST),
  "732490": ProductType(ProductCategory.METALS, WeaponizabilityLikelihood.LOWEST),

  "741300": ProductType(ProductCategory.METALS, WeaponizabilityLikelihood.LOW),
  "741533": ProductType(ProductCategory.METALS, WeaponizabilityLikelihood.LOW),

  "761090": ProductType(ProductCategory.METALS, WeaponizabilityLikelihood.HIGH),
  "761290": ProductType(ProductCategory.METALS, WeaponizabilityLikelihood.LOW),
  "761300": ProductType(ProductCategory.METALS, WeaponizabilityLikelihood.HIGH),

  "810890": ProductType(ProductCategory.METALS, WeaponizabilityLikelihood.HIGH),
  "811229": ProductType(ProductCategory.METALS, WeaponizabilityLikelihood.HIGH),
  "811239": ProductType(ProductCategory.METALS, WeaponizabilityLikelihood.LOW),

  "820220": ProductType(ProductCategory.METALS, WeaponizabilityLikelihood.LOW),
  "820320": ProductType(ProductCategory.METALS, WeaponizabilityLikelihood.LOW),
  "820330": ProductType(ProductCategory.METALS, WeaponizabilityLikelihood.LOW),
  "820810": ProductType(ProductCategory.METALS, WeaponizabilityLikelihood.LOW),
  "820890": ProductType(ProductCategory.METALS, WeaponizabilityLikelihood.LOW),
  "821192": ProductType(ProductCategory.METALS, WeaponizabilityLikelihood.HIGH),
  "821193": ProductType(ProductCategory.METALS, WeaponizabilityLikelihood.HIGH),

  "830241": ProductType(ProductCategory.METALS, WeaponizabilityLikelihood.LOW),
  "830242": ProductType(ProductCategory.METALS, WeaponizabilityLikelihood.LOW),
  "830249": ProductType(ProductCategory.METALS, WeaponizabilityLikelihood.LOW),
  "830710": ProductType(ProductCategory.METALS, WeaponizabilityLikelihood.LOW),

  "840290": ProductType(ProductCategory.MACHINERY, WeaponizabilityLikelihood.LOW),
  "840510": ProductType(ProductCategory.MACHINERY, WeaponizabilityLikelihood.LOW),
  "840590": ProductType(ProductCategory.MACHINERY, WeaponizabilityLikelihood.HIGH),
  "840710": ProductType(ProductCategory.MACHINERY, WeaponizabilityLikelihood.HIGH),
  "840910": ProductType(ProductCategory.MACHINERY, WeaponizabilityLikelihood.HIGH),
  "840991": ProductType(ProductCategory.MACHINERY, WeaponizabilityLikelihood.HIGH),
  "840999": ProductType(ProductCategory.MACHINERY, WeaponizabilityLikelihood.HIGH),
  "841111": ProductType(ProductCategory.MACHINERY, WeaponizabilityLikelihood.HIGH),
  "841181": ProductType(ProductCategory.MACHINERY, WeaponizabilityLikelihood.HIGH),
  "841191": ProductType(ProductCategory.MACHINERY, WeaponizabilityLikelihood.HIGH),
  "841199": ProductType(ProductCategory.MACHINERY, WeaponizabilityLikelihood.HIGH),
  "841221": ProductType(ProductCategory.MACHINERY, WeaponizabilityLikelihood.LOW),
  "841229": ProductType(ProductCategory.MACHINERY, WeaponizabilityLikelihood.LOW),
  "841231": ProductType(ProductCategory.MACHINERY, WeaponizabilityLikelihood.LOW),
  "841239": ProductType(ProductCategory.MACHINERY, WeaponizabilityLikelihood.LOW),
  "841280": ProductType(ProductCategory.MACHINERY, WeaponizabilityLikelihood.HIGH),
  "841290": ProductType(ProductCategory.MACHINERY, WeaponizabilityLikelihood.HIGH),
  "841330": ProductType(ProductCategory.MACHINERY, WeaponizabilityLikelihood.HIGH),
  "842123": ProductType(ProductCategory.MACHINERY, WeaponizabilityLikelihood.HIGH),
  "842131": ProductType(ProductCategory.MACHINERY, WeaponizabilityLikelihood.HIGH),
  "842132": ProductType(ProductCategory.MACHINERY, WeaponizabilityLikelihood.HIGH),
  "842430": ProductType(ProductCategory.MACHINERY, WeaponizabilityLikelihood.LOW),
  "842489": ProductType(ProductCategory.MACHINERY, WeaponizabilityLikelihood.LOW),
  "842890": ProductType(ProductCategory.MACHINERY, WeaponizabilityLikelihood.LOW),
  "843110": ProductType(ProductCategory.MACHINERY, WeaponizabilityLikelihood.LOW),
  "843120": ProductType(ProductCategory.MACHINERY, WeaponizabilityLikelihood.LOW),
  "843139": ProductType(ProductCategory.MACHINERY, WeaponizabilityLikelihood.LOW),
  "843143": ProductType(ProductCategory.MACHINERY, WeaponizabilityLikelihood.HIGH),
  "843149": ProductType(ProductCategory.MACHINERY, WeaponizabilityLikelihood.HIGH),
  "846039": ProductType(ProductCategory.MACHINERY, WeaponizabilityLikelihood.LOW),
  "846791": ProductType(ProductCategory.MACHINERY, WeaponizabilityLikelihood.LOW),
  "847130": ProductType(ProductCategory.MACHINERY, WeaponizabilityLikelihood.LOW),
  "847141": ProductType(ProductCategory.MACHINERY, WeaponizabilityLikelihood.LOW),
  "847149": ProductType(ProductCategory.MACHINERY, WeaponizabilityLikelihood.LOW),
  "847150": ProductType(ProductCategory.MACHINERY, WeaponizabilityLikelihood.LOW),
  "847160": ProductType(ProductCategory.MACHINERY, WeaponizabilityLikelihood.LOW),
  "847170": ProductType(ProductCategory.MACHINERY, WeaponizabilityLikelihood.LOW),
  "847180": ProductType(ProductCategory.MACHINERY, WeaponizabilityLikelihood.LOW),
  "847190": ProductType(ProductCategory.MACHINERY, WeaponizabilityLikelihood.LOW),
  "847190": ProductType(ProductCategory.MACHINERY, WeaponizabilityLikelihood.LOW),
  "847330": ProductType(ProductCategory.MACHINERY, WeaponizabilityLikelihood.LOW),
  "847350": ProductType(ProductCategory.MACHINERY, WeaponizabilityLikelihood.LOW),
  "848710": ProductType(ProductCategory.MACHINERY, WeaponizabilityLikelihood.HIGH),
  
  "850110": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.LOW),
  "850162": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.HIGH),
  "850300": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.HIGH),
  "850610": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.LOW),
  "850650": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.LOW),
  "850680": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.LOW),
  "850720": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.LOW),
  "850730": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.LOW),
  "850750": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.LOW),
  "850760": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.HIGH),
  "851110": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.HIGH),
  "851120": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.HIGH),
  "851130": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.HIGH),
  "851140": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.HIGH),
  "851150": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.HIGH),
  "851180": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.HIGH),
  "851190": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.HIGH),
  "851220": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.HIGH),
  "851230": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.LOW),
  "851240": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.LOW),
  "851290": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.LOW),
  "851310": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.LOW),
  "851390": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.LOW),
  "851711": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.LOW),
  "851713": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.LOW),
  "851718": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.LOW),
  "851761": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.LOW),
  "851762": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.LOW),
  "851769": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.LOW),
  "851771": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.HIGH),
  "851779": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.HIGH),
  "851810": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.LOW),
  "851821": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.LOW),
  "851822": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.LOW),
  "851829": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.LOW),
  "851830": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.LOW),
  "851840": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.LOW),
  "851850": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.LOW),
  "851890": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.LOW),
  "851981": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.LOW),
  "851989": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.LOW),
  "852110": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.LOW),
  "852190": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.LOW),
  "852290": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.LOW),
  "852329": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.LOW),
  "852349": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.LOW),
  "852351": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.HIGH),
  "852352": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.HIGH),
  "852359": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.LOW),
  "852380": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.LOW),
  "852411": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.LOW),
  "852412": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.LOW),
  "852491": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.LOW),
  "852499": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.LOW),
  "852550": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.LOW),
  "852560": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.LOW),
  "852581": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.LOW),
  "852583": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.HIGH),
  "852589": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.LOW),
  "852610": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.HIGH),
  "852691": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.HIGH),
  "852692": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.HIGH),
  "852842": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.HIGH),
  "852852": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.HIGH),
  "852859": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.HIGH),
  "852869": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.LOW),
  "852872": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.LOW),
  "852873": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.HIGH),
  "852910": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.HIGH),
  "852990": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.HIGH),
  "853010": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.LOW),
  "853080": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.HIGH),
  "853090": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.HIGH),
  "853110": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.LOW),
  "853120": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.LOW),
  "853180": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.LOW),
  "853190": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.LOW),
  "853340": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.LOW),
  "853610": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.LOW),
  "853620": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.LOW),
  "853670": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.LOW),
  "854151": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.LOW),
  "854159": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.LOW),
  "854160": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.LOW),
  "854190": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.LOW),
  "854231": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.LOW),
  "854232": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.LOW),
  "854233": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.LOW),
  "854239": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.LOW),
  "854290": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.LOW),
  "854320": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.LOW),
  "854330": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.LOW),
  "854370": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.LOW),
  "854390": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.LOW),
  "854411": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.LOW),
  "854419": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.LOW),
  "854430": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.HIGH),
  "854710": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.LOW),
  "854720": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.LOW),
  "854790": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.LOW),
  "854800": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.LOW),
  "854939": ProductType(ProductCategory.ELECTRONICS, WeaponizabilityLikelihood.LOW),

  "871000": ProductType(ProductCategory.VEHICLES, WeaponizabilityLikelihood.HIGHEST),
  "871200": ProductType(ProductCategory.VEHICLES, WeaponizabilityLikelihood.LOWEST),
  "871310": ProductType(ProductCategory.VEHICLES, WeaponizabilityLikelihood.LOWEST),
  "871491": ProductType(ProductCategory.VEHICLES, WeaponizabilityLikelihood.LOWEST),
  "871492": ProductType(ProductCategory.VEHICLES, WeaponizabilityLikelihood.LOWEST),
  "871495": ProductType(ProductCategory.VEHICLES, WeaponizabilityLikelihood.LOWEST),
  "871499": ProductType(ProductCategory.VEHICLES, WeaponizabilityLikelihood.LOWEST),

  "880521": ProductType(ProductCategory.VEHICLES, WeaponizabilityLikelihood.HIGHEST),

  "900110": ProductType(ProductCategory.INSTRUMENTS, WeaponizabilityLikelihood.LOW),
  "900190": ProductType(ProductCategory.INSTRUMENTS, WeaponizabilityLikelihood.LOW),
  "900211": ProductType(ProductCategory.INSTRUMENTS, WeaponizabilityLikelihood.LOW),
  "900219": ProductType(ProductCategory.INSTRUMENTS, WeaponizabilityLikelihood.LOW),
  "900220": ProductType(ProductCategory.INSTRUMENTS, WeaponizabilityLikelihood.LOW),
  "900290": ProductType(ProductCategory.INSTRUMENTS, WeaponizabilityLikelihood.LOW),
  "900490": ProductType(ProductCategory.INSTRUMENTS, WeaponizabilityLikelihood.LOW),
  "900510": ProductType(ProductCategory.INSTRUMENTS, WeaponizabilityLikelihood.HIGH),
  "900580": ProductType(ProductCategory.INSTRUMENTS, WeaponizabilityLikelihood.LOW),
  "900590": ProductType(ProductCategory.INSTRUMENTS, WeaponizabilityLikelihood.HIGH),
  "900630": ProductType(ProductCategory.INSTRUMENTS, WeaponizabilityLikelihood.LOW),
  "900640": ProductType(ProductCategory.INSTRUMENTS, WeaponizabilityLikelihood.LOW),
  "900661": ProductType(ProductCategory.INSTRUMENTS, WeaponizabilityLikelihood.LOW),
  "900669": ProductType(ProductCategory.INSTRUMENTS, WeaponizabilityLikelihood.LOW),
  "900691": ProductType(ProductCategory.INSTRUMENTS, WeaponizabilityLikelihood.LOW),
  "900710": ProductType(ProductCategory.INSTRUMENTS, WeaponizabilityLikelihood.LOW),
  "900791": ProductType(ProductCategory.INSTRUMENTS, WeaponizabilityLikelihood.LOW),
  "901310": ProductType(ProductCategory.INSTRUMENTS, WeaponizabilityLikelihood.HIGHEST),
  "901320": ProductType(ProductCategory.INSTRUMENTS, WeaponizabilityLikelihood.HIGH),
  "901380": ProductType(ProductCategory.INSTRUMENTS, WeaponizabilityLikelihood.LOW),
  "901390": ProductType(ProductCategory.INSTRUMENTS, WeaponizabilityLikelihood.LOW),
  "901410": ProductType(ProductCategory.INSTRUMENTS, WeaponizabilityLikelihood.HIGH),
  "901420": ProductType(ProductCategory.INSTRUMENTS, WeaponizabilityLikelihood.HIGH),
  "901480": ProductType(ProductCategory.INSTRUMENTS, WeaponizabilityLikelihood.HIGH),
  "901490": ProductType(ProductCategory.INSTRUMENTS, WeaponizabilityLikelihood.HIGH),
  "901510": ProductType(ProductCategory.INSTRUMENTS, WeaponizabilityLikelihood.HIGH),
  "901530": ProductType(ProductCategory.INSTRUMENTS, WeaponizabilityLikelihood.LOW),
  "901580": ProductType(ProductCategory.INSTRUMENTS, WeaponizabilityLikelihood.LOW),
  "901590": ProductType(ProductCategory.INSTRUMENTS, WeaponizabilityLikelihood.LOW),
  "901720": ProductType(ProductCategory.INSTRUMENTS, WeaponizabilityLikelihood.LOW),
  "901730": ProductType(ProductCategory.INSTRUMENTS, WeaponizabilityLikelihood.LOW),
  "901790": ProductType(ProductCategory.INSTRUMENTS, WeaponizabilityLikelihood.LOW),
  "902000": ProductType(ProductCategory.INSTRUMENTS, WeaponizabilityLikelihood.LOW),
  "902410": ProductType(ProductCategory.INSTRUMENTS, WeaponizabilityLikelihood.LOW),
  "903300": ProductType(ProductCategory.INSTRUMENTS, WeaponizabilityLikelihood.LOW),

  "940690": ProductType(ProductCategory.MANUFACTURED, WeaponizabilityLikelihood.HIGH),

  "962000": ProductType(ProductCategory.MANUFACTURED, WeaponizabilityLikelihood.HIGH),

  "980110": ProductType(ProductCategory.SPECIAL, WeaponizabilityLikelihood.HIGH),
  "980310": ProductType(ProductCategory.WEAPONS, WeaponizabilityLikelihood.HIGHEST),
  "980320": ProductType(ProductCategory.WEAPONS, WeaponizabilityLikelihood.HIGHEST),
}


def classify_hs_code(hs_code: str) -> ProductType:
  """Classify an HS code into a product type based on its chapter."""
  code6 = hs_code[:6]
  if code6 in HS_CODE_OVERRIDES:
    return HS_CODE_OVERRIDES[code6]
  chapter = hs_code[:2]
  return HS_CHAPTER_TO_TYPE.get(chapter,  ProductType(ProductCategory.OTHER, False))


def get_category_description(category: ProductType) -> str:
  """Return human-readable description of what HS chapters a category covers."""
  chapters = [ch for ch, typ in HS_CHAPTER_TO_TYPE.items() if typ.category == category]
  chapters.sort()
  return f"{category.value}: HS chapters {', '.join(chapters)}"