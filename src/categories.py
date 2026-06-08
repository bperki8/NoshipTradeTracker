"""Maps HS (Harmonized System) code chapters to product categories.

HS codes are 6-10 digit international commodity codes. The first 2 digits
(the chapter) broadly identify the product type. This module maps those
chapters to our simplified product categories for analysis.

https://hts.usitc.gov/
"""

from .models import ProductCategory, ProductType

# HS chapter (first 2 digits) to ProductCategory mapping.
# See Table of Contents here: https://hts.usitc.gov/
# TODO: Update the description and lists in the README.
# TODO: Should we go into more detail for some of these than just the two number chapter?
HS_CHAPTER_TO_TYPE: dict[str, ProductType] = {
  # Section I LIVE ANIMALS; ANIMAL PRODUCTS
  "01": ProductType(ProductCategory.ANIMALS, False),  # Live animals
  "02": ProductType(ProductCategory.ANIMALS, False),  # Meat and edible meat offal
  "03": ProductType(ProductCategory.ANIMALS, False),  # Fish and crustaceans, molluscs and other aquatic invertebrates
  "04": ProductType(ProductCategory.ANIMALS, False),  # Dairy produce; birds´ eggs; natural honey; edible products of animal origin, not elsewhere specified or included
  "05": ProductType(ProductCategory.ANIMALS, False),  # Products of animal origin, not elsewhere specified or included
  # Section II VEGETABLE PRODUCTS
  "06": ProductType(ProductCategory.PLANTS, False),   # Live trees and other plants; bulbs, roots and the like; cut flowers and ornamental foliage
  "07": ProductType(ProductCategory.PLANTS, False),   # Edible vegetables and certain roots and tubers
  "08": ProductType(ProductCategory.PLANTS, False),   # Edible fruit and nuts; peel of citrus fruit or melons
  "09": ProductType(ProductCategory.PLANTS, False),   # Coffee, tea, maté and spices
  "10": ProductType(ProductCategory.PLANTS, False),   # Cereals
  "11": ProductType(ProductCategory.PLANTS, False),   # Products of the milling industry; malt; starches; inulin; wheat gluten
  # TODO: This includes "medicinal plants". Should we count this as "potentially weaponizable"? Should we use levels of weaponizability?
  "12": ProductType(ProductCategory.PLANTS, False),   # Oil seeds and oleaginous fruits; miscellaneous grains, seeds and fruit; industrial or medicinal plants; straw and fodder
  # TODO: What are resins used for?
  "13": ProductType(ProductCategory.PLANTS, False),   # Lac; gums; resins and other vegetable saps and extracts
  "14": ProductType(ProductCategory.PLANTS, False),   # Vegetable plaiting materials; vegetable products not elsewhere specified or included
  # SECTION III ANIMAL, VEGETABLE OR MICROBIAL FATS AND OILS AND THEIR CLEAVAGE PRODUCTS; PREPARED EDIBLE FATS; ANIMAL OR VEGETABLE WAXES
  "15": ProductType(ProductCategory.ANIMALS, False),   # Animal, vegetable or microbial fats and oils and their cleavage products; prepared edible fats; animal or vegetable waxes
  # SECTION IV PREPARED FOODSTUFFS; BEVERAGES, SPIRITS AND VINEGAR; TOBACCO AND MANUFACTURED TOBACCO SUBSTITUTES; PRODUCTS, WHETHER OR NOT CONTAINING NICOTINE, INTENDED FOR INHALATION WITHOUT COMBUSTION; OTHER NICOTINE CONTAINING PRODUCTS INTENDED FOR THE INTAKE OF NICOTINE INTO THE HUMAN BODY
  "16": ProductType(ProductCategory.ANIMALS, False),  # Preparations of meat, of fish, of crustaceans, molluscs or other aquatic invertebrates, or of insects
  "17": ProductType(ProductCategory.PLANTS, False),   # Sugars and sugar confectionery
  "18": ProductType(ProductCategory.PLANTS, False),   # Cocoa and cocoa preparations
  "19": ProductType(ProductCategory.PLANTS, False),   # Preparations of cereals, flour, starch or milk; bakers' wares
  "20": ProductType(ProductCategory.PLANTS, False),   # Preparations of vegetables, fruit, nuts or other parts of plants
  "21": ProductType(ProductCategory.ANIMALS, False),   # Miscellaneous edible preparations
  "22": ProductType(ProductCategory.PLANTS, False),   # Beverages, spirits and vinegar
  "23": ProductType(ProductCategory.ANIMALS, False),  # Residues and waste from the food industries; prepared animal feed
  "24": ProductType(ProductCategory.PLANTS, False),   # Tobacco and manufactured tobacco substitutes; products whether or not containing nicotine, intended for inhalation without combustion; other nicotine containing products intended for the intake of nicotine into the human body
  # SECTION V MINERAL PRODUCTS
  # TODO: Is the stuff in this Minerals section weaponizable? Putting "No" for now.
  "25": ProductType(ProductCategory.MINERALS, False), # Salt; sulfur; earths and stone; plastering materials, lime and cement
  "26": ProductType(ProductCategory.MINERALS, False), # Ores, slag, ash
  "27": ProductType(ProductCategory.MINERALS, False), # Mineral fuels, mineral oils and products of their distillation; bituminous substances; mineral waxes
  # SECTION VI PRODUCTS OF THE CHEMICAL OR ALLIED INDUSTRIES
  # TODO: Radioactive elements and precious metals sound weaponizable to me. Agreed?
  "28": ProductType(ProductCategory.CHEMICALS, True),  # Inorganic chemicals; organic or inorganic compounds of precious metals, of rare-earth metals, of radioactive elements or of isotopes
  "29": ProductType(ProductCategory.CHEMICALS, False),  # Organic chemicals
  # TODO: Should we count all health products as weaponizable? Israel does when they blockade supplies from getting into Palestine.
  "30": ProductType(ProductCategory.HEALTH, False),     # Pharmaceutical products
  "31": ProductType(ProductCategory.CHEMICALS, False),  # Fertilizers
  "32": ProductType(ProductCategory.CHEMICALS, False),  # Tanning or dyeing extracts; tannins and their derivatives; dyes, pigments and other coloring matter; paints and varnishes; putty and other mastics; inks
  "33": ProductType(ProductCategory.CHEMICALS, False),     # Essential oils and resinoids; perfumery, cosmetic or toilet preparations
  "34": ProductType(ProductCategory.CHEMICALS, False),  # Soap, organic surface-active agents, washing preparations, lubricating preparations, artificial waxes, prepared waxes, polishing or scouring preparations, candles and similar articles, modeling pastes,"dental waxes" and dental preparations with a basis of plaster
  "35": ProductType(ProductCategory.CHEMICALS, False),  # Albuminoidal substances; modified starches; glues; enzymes
  "36": ProductType(ProductCategory.CHEMICALS, True),  # Explosives; pyrotechnic products; matches; pyrophoric alloys; certain combustible preparations
  "37": ProductType(ProductCategory.CHEMICALS, False),  # Photographic or cinematographic goods
  "38": ProductType(ProductCategory.CHEMICALS, False),  # Miscellaneous chemical products
  # SECTION VII PLASTICS AND ARTICLES THEREOF; RUBBER AND ARTICLES THEREOF
  # TODO: Are plastics and rubber weaponizable?
  "39": ProductType(ProductCategory.PLASTICS_RUBBER, False), # Plastics and articles thereof
  "40": ProductType(ProductCategory.PLASTICS_RUBBER, False), # Rubber and articles thereof
  # SECTION VIII RAW HIDES AND SKINS, LEATHER, FURSKINS AND ARTICLES THEREOF; SADDLERY AND HARNESS; TRAVEL GOODS, HANDBAGS AND SIMILAR CONTAINERS; ARTICLES OF ANIMAL GUT (OTHER THAN SILKWORM GUT)
  "41": ProductType(ProductCategory.ANIMALS, False),  # Raw hides and skins (other than furskins) and leather
  "42": ProductType(ProductCategory.ANIMALS, False),  # Articles of leather; saddlery and harness; travel goods, handbags and similar containers; articles of animal gut (other than silkworm gut)
  "43": ProductType(ProductCategory.ANIMALS, False),  # Furskins and artificial fur; manufactures thereof
  # SECTION IX WOOD AND ARTICLES OF WOOD;WOOD CHARCOAL; CORK AND ARTICLES OF CORK; MANUFACTURES OF STRAW, OF ESPARTO OR OF OTHER PLAITING MATERIALS; BASKETWARE AND WICKERWORK
  "44": ProductType(ProductCategory.WOOD_PAPER, False), # Wood and articles of wood; wood charcoal
  "45": ProductType(ProductCategory.WOOD_PAPER, False), # Cork and articles of cork
  "46": ProductType(ProductCategory.WOOD_PAPER, False), # Manufactures of straw, of esparto or of other plaiting materials; basketware and wickerwork
  # SECTION X PULP OF WOOD OR OF OTHER FIBROUS CELLULOSIC MATERIAL; RECOVERED (WASTE AND SCRAP) PAPER OR PAPERBOARD; PAPER AND PAPERBOARD AND ARTICLES THEREOF
  "47": ProductType(ProductCategory.WOOD_PAPER, False), # Pulp of wood or of other fibrous cellulosic material; recovered (waste and scrap) paper or paperboard
  "48": ProductType(ProductCategory.WOOD_PAPER, False), # Paper and paperboard; articles of paper pulp, of paper or of paperboard
  "49": ProductType(ProductCategory.WOOD_PAPER, False), # Printed books, newspapers, pictures and other products of the printing industry; manuscripts, typescripts and plans
  # SECTION XI TEXTILES AND TEXTILE ARTICLES
  # TODO: Potentially undercounting animal exploitation in this section.
  "50": ProductType(ProductCategory.ANIMALS, False),  # Silk
  "51": ProductType(ProductCategory.ANIMALS, False),  # Wool, fine or coarse animal hair; horsehair yarn and woven fabric
  "52": ProductType(ProductCategory.TEXTILES, False), # Cotton
  "53": ProductType(ProductCategory.TEXTILES, False), # Other vegetable textile fibers; paper yarn and woven fabrics of paper yarn
  "54": ProductType(ProductCategory.TEXTILES, False), # Man-made filaments; strip and the like of man-made textile materials
  "55": ProductType(ProductCategory.TEXTILES, False), # Man-made staple fibers
  "56": ProductType(ProductCategory.TEXTILES, False), # Wadding, felt and nonwovens; special yarns; twine, cordage, ropes and cables and articles thereof
  "57": ProductType(ProductCategory.TEXTILES, False), # Carpets and other textile floor coverings
  "58": ProductType(ProductCategory.TEXTILES, False), # Special woven fabrics; tufted textile fabrics; lace; tapestries; trimmings; embroidery
  "59": ProductType(ProductCategory.TEXTILES, False), # Impregnated, coated, covered or laminated textile fabrics; textile articles of a kind suitable for industrial use
  "60": ProductType(ProductCategory.TEXTILES, False), # Knitted or crocheted fabrics
  "61": ProductType(ProductCategory.TEXTILES, False), # Articles of apparel and clothing accessories, knitted or crocheted
  "62": ProductType(ProductCategory.TEXTILES, False), # Articles of apparel and clothing accessories, not knitted or crocheted
  "63": ProductType(ProductCategory.TEXTILES, False), # Other made up textile articles; needlecraft sets; worn clothing and worn textile articles; rags
  # SECTION XII FOOTWEAR, HEADGEAR, UMBRELLAS, SUN UMBRELLAS, WALKING-STICKS, SEAT-STICKS, WHIPS, RIDING-CROPS AND PARTS THEREOF; PREPARED FEATHERS AND ARTICLES MADE THEREWITH; ARTIFICIAL FLOWERS; ARTICLES OF HUMAN HAIR
  # TODO: Should we mark some of these as weaponizable? Could they be hiding military gear/apparel?
  "64": ProductType(ProductCategory.TEXTILES, False), # Footwear, gaiters and the like; parts of such articles
  "65": ProductType(ProductCategory.TEXTILES, False), # Headgear and parts thereof 
  "66": ProductType(ProductCategory.TEXTILES, False), # Umbrellas, sun umbrellas, walking-sticks, seat-sticks, whips, riding-crops and parts thereof
  "67": ProductType(ProductCategory.ANIMALS, False), # Prepared feathers and down and articles made of feathers or of down; artificial flowers; articles of human hair
  # SECTION XIII ARTICLES OF STONE, PLASTER, CEMENT, ASBESTOS, MICA OR SIMILAR MATERIALS; CERAMIC PRODUCTS; GLASS AND GLASSWARE
  "68": ProductType(ProductCategory.STONE_CERAMIC_GLASS, False), # Articles of stone, plaster, cement, asbestos, mica or similar materials
  "69": ProductType(ProductCategory.STONE_CERAMIC_GLASS, False), # Ceramic products
  "70": ProductType(ProductCategory.STONE_CERAMIC_GLASS, False), # Glass and glassware
  # SECTION XIV NATURAL OR CULTURED PEARLS, PRECIOUS OR SEMIPRECIOUS STONES, PRECIOUS METALS, METALS CLAD WITH PRECIOUS METAL, AND ARTICLES THEREOF; IMITATION JEWELRY; COIN
  # TODO: Can precious metals be weaponized?
  "71": ProductType(ProductCategory.METALS, False), # Natural or cultured pearls, precious or semiprecious stones, precious metals, metals clad with precious metal, and articles thereof; imitation jewelry; coin
  # SECTION XV BASE METALS AND ARTICLES OF BASE METAL
  # Which metals can and which can't be weaponized? Just going by vibes right now. lol
  "72": ProductType(ProductCategory.METALS, False), # Iron and steel
  "73": ProductType(ProductCategory.METALS, False), # Articles of iron or steel
  "74": ProductType(ProductCategory.METALS, False), # Copper and articles thereof
  "75": ProductType(ProductCategory.METALS, False), # Nickel and articles thereof
  "76": ProductType(ProductCategory.METALS, False), # Aluminum and articles thereof
  # "77": (Reserved for possible future use)
  "78": ProductType(ProductCategory.METALS, False), # Lead and articles thereof
  "79": ProductType(ProductCategory.METALS, False), # Zinc and articles thereof
  "80": ProductType(ProductCategory.METALS, False), # Tin and articles thereof
  "81": ProductType(ProductCategory.METALS, False), # Other base metals; cermets; articles thereof
  # TODO: Tools is broad. Weaponizable? Putting no for now.
  "82": ProductType(ProductCategory.METALS, False), # Tools, implements, cutlery, spoons and forks, of base metal; parts thereof of base metal
  "83": ProductType(ProductCategory.METALS, False), # Miscellaneous articles of base metal
  # SECTION XVI MACHINERY AND MECHANICAL APPLIANCES; ELECTRICAL EQUIPMENT; PARTS THEREOF; SOUND RECORDERS AND REPRODUCERS, TELEVISION IMAGE AND SOUND RECORDERS AND REPRODUCERS, AND PARTS AND ACCESSORIES OF SUCH ARTICLES
  # TODO: Nuclear reactors!?!
  "84": ProductType(ProductCategory.MACHINERY, True), # Nuclear reactors, boilers, machinery and mechanical appliances; parts thereof
  "85": ProductType(ProductCategory.ELECTRONICS, False), # Electrical machinery and equipment and parts thereof; sound recorders and reproducers, television image and sound recorders and reproducers, and parts and accessories of such articles
  # SECTION XVII VEHICLES, AIRCRAFT, VESSELS AND ASSOCIATED TRANSPORT EQUIPMENT
  "86": ProductType(ProductCategory.VEHICLES, True), # Railway or tramway locomotives, rolling stock and parts thereof; railway or tramway track fixtures and fittings and parts thereof; mechanical (including electro-mechanical) traffic signaling equipment of all kinds
  "87": ProductType(ProductCategory.VEHICLES, True), # Vehicles other than railway or tramway rolling stock, and parts and accessories thereof
  "88": ProductType(ProductCategory.VEHICLES, True), # Aircraft, spacecraft, and parts thereof
  "89": ProductType(ProductCategory.VEHICLES, True), # Ships, boats and floating structures
  # SECTION XVIII OPTICAL, PHOTOGRAPHIC, CINEMATOGRAPHIC, MEASURING, CHECKING, PRECISION, MEDICAL OR SURGICAL INSTRUMENTS AND APPARATUS; CLOCKS AND WATCHES; MUSICAL INSTRUMENTS; PARTS AND ACCESSORIES THEREOF
  # TODO: Same question from above about whether medical supplies count as weaponisable. Saying yes for now.
  "90": ProductType(ProductCategory.HEALTH, False), # Optical, photographic, cinematographic, measuring, checking, precision, medical or surgical instruments and apparatus; parts and accessories thereof
  "91": ProductType(ProductCategory.INSTRUMENTS, False), # Clocks and watches and parts thereof
  "92": ProductType(ProductCategory.INSTRUMENTS, False), # Musical instruments; parts and accessories of such articles
  # SECTION XIX ARMS AND AMMUNITION; PARTS AND ACCESSORIES THEREOF
  "93": ProductType(ProductCategory.WEAPONS, True), # Arms and ammunition; parts and accessories thereof
  # SECTION XX MISCELLANEOUS MANUFACTURED ARTICLES
  "94": ProductType(ProductCategory.MANUFACTURED, False), # Furniture; bedding, mattresses, mattress supports, cushions and similar stuffed furnishings; luminaires and lighting fittings, not elsewhere specified or included; illuminated signs, illuminated nameplates and the like; prefabricated buildings
  "95": ProductType(ProductCategory.MANUFACTURED, False), # Toys, games and sports equipment; parts and accessories thereof
  # TODO: Potentially weaponizable? Should do more research.
  "96": ProductType(ProductCategory.MANUFACTURED, False), # Miscellaneous manufactured articles
  # SECTION XXI WORKS OF ART, COLLECTORS' PIECES AND ANTIQUES
  "97": ProductType(ProductCategory.ART, False), # Works of art, collectors' pieces and antiques
  # SECTION XXII SPECIAL CLASSIFICATION PROVISIONS; TEMPORARY LEGISLATION; TEMPORARY MODIFICATIONS ESTABLISHED PURSUANT TO TRADE LEGISLATION; ADDITIONAL IMPORT RESTRICTIONS ESTABLISHED PURSUANT TO SECTION 22 OF THE AGRICULTURAL ADJUSTMENT ACT, AS AMENDED
  # TODO: Might be worthwhile to look into these if there are a lot.
  # TODO: I found that 9803, 980310, and 980320 are special provisions for Military apparel/equipment. Gonna have to figure out how to short circuit these and mark them as weaponizable.
  "98": ProductType(ProductCategory.SPECIAL, False), # Special classification provisions
  "99": ProductType(ProductCategory.SPECIAL, False), # Temporary legislation; temporary modifications established pursuant to trade legislation; additional import restrictions established pursuant to section 22 of the Agricultural Adjustment Act, as amended
}


def classify_hs_code(hs_code: str) -> ProductType:
  """Classify an HS code into a product type based on its chapter."""
  chapter = hs_code[:2]
  # For debugging:
  # product_type = HS_CHAPTER_TO_TYPE.get(chapter,  ProductType(ProductCategory.OTHER, False))
  # if product_type.category == ProductCategory.OTHER:
  #   print(f"!!! hs_code = {hs_code} and chapter = {chapter} and product_type = {product_type} !!!")
  # return product_type
  return HS_CHAPTER_TO_TYPE.get(chapter,  ProductType(ProductCategory.OTHER, False))


def get_category_description(category: ProductType) -> str:
  """Return human-readable description of what HS chapters a category covers."""
  chapters = [ch for ch, typ in HS_CHAPTER_TO_TYPE.items() if typ.category == category]
  chapters.sort()
  return f"{category.value}: HS chapters {', '.join(chapters)}"