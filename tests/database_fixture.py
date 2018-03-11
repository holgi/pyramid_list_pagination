''' database setup and example data for tests '''

import pytest

from sqlalchemy import engine_from_config, Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import MetaData

NAMING_CONVENTION = {
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(constraint_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s'
    }

# setup metadata conventions and base declarative class
metadata = MetaData(naming_convention=NAMING_CONVENTION)
Base = declarative_base(metadata=metadata)


class Cheese(Base):
    ''' A cheese '''

    __tablename__ = 'cheeses'

    #: primary key
    id = Column(Integer, primary_key=True)
    #: country of origin
    country = Column(Text, nullable=False)
    #: name of the cheese
    name = Column(Text, nullable=False)
    #: region it is produced
    region = Column(Text, nullable=False)
    #: description
    description = Column(Text, nullable=False)


# the list of cheeses was assembled from
# https://en.wikipedia.org/wiki/List_of_cheeses and other pages
# in the domain of en.wikipedia.org
cheeses = [
    ('Belgium', 'Passendale cheese', 'Passendale', '''Named after Passendale, the village where it originated, it is one of the best-known cheeses in Belgium. It resembles a loaf of bread and has a round shape and a hard, but edible brown rind with spots of white. Inside, the flesh is golden, dotted with small holes and very creamy. It has a firm and damp consistency, slightly sweet bouquet and mild flavor. The regular Passendale cheese exists in two variations called Passendale Classic and Passendale Prelude.[21]'''),  # noqa: E501
    ('Belgium', 'Remoudou', 'Land of Herve', '''It derives its name from the use of milk removed 15 minutes after the usual milking. Hence the wallon verbrimoûd meaning to re-milk.[22] This cheese weighs 200 to 500g. When it is washed with salt it gets a strong taste, and when it is washed with milk it keeps a mild taste. It is often sold in pieces.'''),  # noqa: E501
    ('Belgium', 'Rodoric', 'Liège', '''An aged cheese made from unpasteurized goat milk that is traditionally aged in humid caves. When young, the interior is sweet, with age the flavor becomes spicy.'''),  # noqa: E501
    ('Bosnia and Herzegovina', 'Livno cheese', 'Livno', '''The cheese is ready after an average of 60 to 66 days in a controlled environment. The flavor is full, and in older cheeses the taste is slightly piquant. The largest producer is Mljekara Livno or Lura Dairy d.o.o. Livno, with yearly production exceeding 500 metric tons.'''),  # noqa: E501
    ('Bosnia and Herzegovina', 'Travnički (Vlašić) cheese', 'Travnik', '''This cheese is produced on Vlašić mountain in central Bosnia, above the city of Travnik. It was originally made from sheep milk, but there are varieties made from cow milk. This cheese is white in color, and can either have small irregular holes scattered in it, or be solid without holes. Its taste is dry and salty. The milk has a special taste that comes from the variety of different herbs that sheep are eating while grazing on the mountain.'''),  # noqa: E501
    ('Bulgaria', 'Cherni Vit', 'Teteven Municipality, Lovech Province', '''Made from sheep milk, Cherni Vit cheese owes the green color of its crust and its characteristic taste to the formation of mold. This occurs naturally due to the specific conditions in the region and the technology of production. Produced for centuries, Cherni Vit cheese was nearly extinct in the 2000s until it was rediscovered and popularized by Slow Food representatives.'''),  # noqa: E501
    ('Croatia', 'Paški sir', 'Island of Pag', '''A hard, distinctively flavored sheep milk cheese. It is generally regarded as the most famous of Croatian artisan cheeses and is found in many export markets outside Croatia, also known as Godsips cheese.'''),  # noqa: E501
    ('Czech Republic', 'Olomoucké syrečky', 'Loštice', '''A ripened soft cheese that is easily recognizable per its strong scent and yellowish color. It is named after the city of Olomouc and contains only 0.6% of fat.'''),  # noqa: E501
    ('Denmark', 'Maribo', 'Lolland', '''A semi-hard cheese made from cow's milk. It has a firm, dry interior; a creamy texture; and many small, irregular holes. It has a pale tan rind covered in yellow wax. Its flavour is tangy, and it is sometimes seasoned with caraway seeds.'''),  # noqa: E501
    ('Denmark', 'Molbo', 'Mols', '''A semi-hard cow's milk cheese made in the region of Mols. It is very similar to Edam, with a delicate, light flavour that is slightly tangy and salty. It has small, regular holes and is covered in a red wax coating.'''),  # noqa: E501
    ('Denmark', 'Samsø cheese', 'Samsø', '''A cow's milk cheese named after the island of Samsø. It is similar to Emmentaler, although its flavour is milder: gentle and nutty in young cheeses and pungent with sweet and sour notes in older ones. Samsø's interior has a supple, elastic texture; a yellow colour; and a few large, irregular holes. It is the national cheese of Denmark.'''),  # noqa: E501
    ('Estonia', 'Kadaka juust', 'Saaremaa', '''Semi hard smoked cheese made from cow's milk, produced by Saaremaa Piimatööstus. Also available with garlic.'''),  # noqa: E501
    ('Finland', 'Lappi', 'Lapland', '''Made from partially skimmed cow's milk, similar to Emmental except that it is pasteurized.'''),  # noqa: E501
    ('Finland', 'Leipäjuusto', 'Southern Ostrobothnia, Kainuu', '''Fresh cheese made from cow's beestings. Sometimes made from goat or reindeer milk.'''),  # noqa: E501
    ('Greece', 'Feta', 'Epirus, Macedonia, Thrace, Thessaly, Peloponnese, Lesbos', '''Feta is a brined curd white cheese made only in Greece. It is made from sheep's milk, or from a mixture of sheep and goat's milk. The word "feta" in Greek means "slice".[31]'''),  # noqa: E501
    ('Greece', 'Graviera', 'Agrafa, Crete, Naxos', '''Graviera is a type of Greek hard yellow cheese. It is made exclusively from sheep or goat milk.'''),  # noqa: E501
    ('Greece', 'Malaka', 'Crete', '''Also known as Tiromalama. Made from Graviera curd.'''),  # noqa: E501
    ('Greece', 'Tyrozouli', 'Crete', '''Made from Myzithra by adding salt, causing dehydration, and allowing maturation.'''),  # noqa: E501
    ('Malta', 'Ġbejna', 'Commonly associated with the island of Gozo', '''A small round cheese made from sheep's milk, salt and rennet, Ġbejniet are prepared and served in a variety of forms. Until the early 20th century, ġbejniet made from unpasteurised milk were one of the causes of the spread of Brucellosis which was so prevalent as to be called "the Maltese fever".'''),  # noqa: E501
    ('Portugal', 'Castelo Branco cheese', 'Beira Baixa', '''a cheese named after the city of the same name in Portugal, the main city of the district where it is produced. The cheese is made from milk produced by either a goat or a ewe, and has a soft texture.'''),  # noqa: E501
    ('Portugal', 'Queijo de Nisa', 'Alto Alentejo', '''a semi-hard sheep's milk cheese from the municipality of Nisa. It is created from raw milk, which is coagulated, then curdled using an infusion of thistle.'''),  # noqa: E501
    ('Portugal', 'Queijo do Pico', 'Azores', '''Originating from the island of Pico, this cured cheese is produced in cylindrical formats from cow milk It is considered a fatty cheese and the ripening of the cheese forms a yellow exterior irregular crust and yellowish-white, soft and pasty interior. Pico cheese has a salty taste and a, characteristically, intense aroma.'''),  # noqa: E501
    ('Portugal', 'Queijo de Azeitão', 'Azeitão, Setúbal', '''Sheep's milk cheese originating from the town of Azeitão.'''),  # noqa: E501
    ('Portugal', 'São Jorge', 'Azores', '''Produced in the São Jorge Island, this is a hard/semi-hard cheese made from unpasteurised cow's milk, and the pâte has small eyes.'''),  # noqa: E501
    ('Portugal', 'Serra da Estrela', 'Serra da Estrela', '''Produced in a mountainous region this cheeses is made from sheep's milk, mostly during the months of November to March. The texture of the paste varies depending on its age, from a very soft semi-liquid when young, to a soft but sliceable solid when older. It is a cured cheese created by artisanal producers with a white or slightly yellow color and a uniform creamy consistency with at most a few small holes in it.'''),  # noqa: E501
    ('Slovakia', 'Korbáčiky', 'Orava', '''A type of string cheese made from steamed cheese interwoven into fine braids. Common flavors include salty, smoked and garlic.'''),  # noqa: E501
    ('Slovenia', 'Tolminc cheese', 'Tolmin', '''Made with raw cow milk, it has a sweet and spicy flavor. The cheese is registered as a Protected Designation of Origin.[43]'''),  # noqa: E501
    ('Sweden', 'Blå Gotland', 'Stånga', '''Gotland Blue is made in Sweden by the Arla Foods company in the town of Stånga on the island of Gotland. This cheese is often characterized as being somewhere between strong and mild, containing elements of both types. The color is a pale yellow, and it has no holes.'''),  # noqa: E501
    ('Sweden', 'Moose cheese', 'Bjurholm, Sweden', '''A cheese produced in Sweden from moose milk'''),  # noqa: E501
    ('Sweden', 'Västerbottensost', 'Burträsk', '''A hard cow's milk cheese with tiny eyes or holes and a firm and granular texture. Strong in flavour, its taste is described as somewhat like Parmesan cheese, salty, but with more bitter notes. Västerbotten cheese must be aged for at least 12 months.'''),  # noqa: E501
    ('Iran', 'Lighvan cheese', 'Liqvan', '''a brined curd cheese traditionally made in Iran. Having a sour flavor, and a shape covered by holes, the cheese is produced from sheep's milk. The name comes from Liqvan, a village in Tabriz, where it has traditionally been made.'''),  # noqa: E501
    ('Iran', 'Talesh cheese', 'Talesh', '''it can only be found in Talesh county. this cheese is made from goat or sheep milk. Once the cheese is processed, it is held in sheep or goat skin for aging and preservation.'''),  # noqa: E501
    ('Iran', 'Mahali cheese', 'Mazandaran', '''This cheese is very similar to Indian Paneer. It is made from full fat cow's milk. It tastes mild and is kept in salt brine.'''),  # noqa: E501
    ('Israel', 'Tzfatit Kasheh', 'Upper Galilee', '''Hard texture Savory flavor; perfect for grating on top of Shakshouka'''),  # noqa: E501
    ('Israel', 'Tzfatit Tari', 'Upper Galilee', '''Mild flavor; texture ranges from creamy to firm'''),  # noqa: E501
    ('Levant', 'Akkawi', 'Acre', '''A white brine cheese. It is named after the city of Acre, where it first originated, and is commonly made using cow milk, but can be also be made with goat or sheep's milk.'''),  # noqa: E501
    ('Levant', 'Areesh', 'Originated in Egypt', '''It is similar to cottage cheese. Shanklish, a fermented cheese, is made from areesh cheese.[45]'''),  # noqa: E501
    ('Levant', 'Nabulsi cheese', 'Nablus', '''One of a number of Palestinian white brined cheeses made in the Middle East. Its name denotes its place of origin, Nablus[47] and it is well known throughout the West Bank and surrounding regions.'''),  # noqa: E501
    ('Levant', 'Tzfat cheese', 'Safed', '''A semi-hard cheese produced in Israel from sheep's milk. It was first produced by the Meiri dairy in Safed in 1840 and is still produced there by descendants of the original cheese makers.'''),  # noqa: E501
    ('United States', 'Colorado Blackie', 'Colorado', '''A cheese from the American West named for its black waxed rind.'''),  # noqa: E501
    ('United States', 'Red Hawk', 'Northern California', '''A soft, mildly salty cheese'''),  # noqa: E501
    ('Chile', 'Panquehue', 'Andean Aconcagua region', '''A semi-soft cheese, it is one of the most popular cheeses in Chile, it is similar in taste to Tilsit and often has chives or red pepper flakes mixed in.[54][55]'''),  # noqa: E501
    ('Venezuela', 'Guayanés cheese', 'Guayana Region', '''A soft, salty, white cheese.'''),  # noqa: E501
    ('France', 'Brie de Meaux', 'Île-de-France', '''Brie de Meaux is made from cow's milk, with an average weight of 2.8 kg (6.2 lb) for a diameter of 36 to 37 cm (14 to 15 in). It has a soft, delicate white rind. The interior of the cheese is straw-yellow, creamy and soft.'''),  # noqa: E501
    ('France', 'Camembert de Normandie', 'Normandy', '''a moist, soft, creamy, surface-ripened cow's milk cheese. It was first made in the late 18th century at Camembert, Normandy, in northern France.'''),  # noqa: E501
    ('France', 'Époisses de Bourgogne', 'Burgundy', '''Commonly referred to as Époisses, it is a pungent soft-paste cows-milk cheese. Smear-ripened, 'washed rind' (washed in brine and marc de Bourgogne, the local pomace brandy),  # noqa: E501 it is circular at around either 10 cm (3.9 in) or 18 cm (7.1 in) in diameter, with a distinctive soft red-orange color. It is made either from raw or pasteurized milk. It is sold in a circular wooden box, and in restaurants, is sometimes served with a spoon due to its extremely soft texture. The cheese is often paired with Trappist beer or even Sauternes rather than a red wine.'''),  # noqa: E501
    ('France', 'Livarot', 'Normandy', '''It is a soft, pungent, washed rind cheese made from cow's milk. The normal weight for a round of Livarot is 450 g, though it also comes in other weights. It is sold in cylindrical form with the orangish rind wrapped in 3 to 5 rings of dried reedmace '''),  # noqa: E501
    ('France', 'Munster or Munster-Géromé', 'Alsace and Vosges départements in Lorraine (region)', '''a strong smelling, soft cheese with a subtle taste, made mainly from milk from the Vosges, between Alsace, Lorraine and Franche-Comté in France. Muenster is derived from the Alsace town of Muenster, where, among Vosgian abbeys and monasteries, the cheese was conserved and matured in monks' cellars.'''),  # noqa: E501
    ('France', '''Pont-l'Évêque''', 'Normandy', '''Pont-l'Évêque is an uncooked, unpressed cow's-milk cheese, square in shape usually at around 10 cm (3.9 in) square and around 3 cm (1.2 in) high, weighing 400 grams (14 oz). The central pâte is soft, creamy pale yellow in color with a smooth, fine texture and has a pungent aroma. This is surrounded by a washed rind that is white with a gentle orange-brown coloration.'''),  # noqa: E501
    ('France', 'Roquefort', 'Midi-Pyrénées', '''The cheese is white, tangy, crumbly and slightly moist, with distinctive veins of blue mold. It has characteristic odor and flavor with a notable taste of butyric acid; the blue veins provide a sharp tang. It has no rind; the exterior is edible and slightly salty. A typical wheel of Roquefort weighs between 2.5 and 3 kg (5.5 and 6.6 lb),  # noqa: E501 and is about 10 cm (4 in) thick. Each kilogram of finished cheese requires about 4.5 liters (1.2 U.S. gal) of milk to produce. Roquefort is known in France as the king of cheeses.'''),  # noqa: E501
    ('France', 'Tomme de Savoie and Haute-Savoie', 'Savoie', '''a mild, semi-firm cow's milk cheese with a beige interior and a thick brownish-grey rind. Tomme de Savoie dates back to ancient history.'''),  # noqa: E501
    ('Germany', 'Allgäuer Bergkäse', 'Allgäu ', '''from unpasteurized cow's milk, it is ripened for a minimum of four months and has a smooth texture.'''),  # noqa: E501
    ('Germany', 'Handkäse', 'Hesse', '''a regional sour milk cheese (similar to Harzer) and is a culinary speciality of southern Hesse. It gets its name from the traditional way of producing it: forming it with one's own hands.'''),  # noqa: E501
    ('Germany', 'Harzer', 'Harz', '''a sour milk cheese made from low fat curd cheese, which contains only about one percent fat'''),  # noqa: E501
    ('Germany', 'Hirtenkäse', 'Allgäu ', '''a distinctive golden-colored, hard cow's milk cheese made in the Allgäu area of Southern Germany'''),  # noqa: E501
    ('Germany', 'Obatzda', 'Bavaria', '''prepared by mixing two thirds aged soft cheese, usually Camembert (Romadur or similar cheeses may be used as well) and one third butter.'''),  # noqa: E501
    ('Italy', 'Bra', 'Piemonte', '''The cheese may use either unpasteurized or pasteurized milk, often entirely cow's milk, but goat's or sheep's milk may be added in small amounts. It may be served as a soft or hard cheese, depending on the length of aging, from at least forty five days for soft cheese, from six months for hard cheese.'''),  # noqa: E501
    ('Italy', 'Canestrato Pugliese', 'Puglia', '''Canestrato is a hard cheese from the Italian regions of Basilicata, Apulia, Sicily, and Abruzzo, made from a mixture of sheep milk and goat milk. '''),  # noqa: E501
    ('Italy', 'Gorgonzola', 'Lombardy, Piedmont', '''a veined Italian blue cheese, made from unskimmed cow's milk. It can be buttery or firm, crumbly and quite salty, with a "bite" from its blue veining'''),  # noqa: E501
    ('Italy', 'Mozzarella di Bufala ', 'Campania', '''a mozzarella made from the milk of Mediterranea Italiana buffalo.'''),  # noqa: E501
    ('Italy', 'Pecorino Sardo', 'Sardinia', '''Its flavour is different from that of the Pecorino Romano, which is also made on the island. Sardo is richer while romano is much more biting and salty. Pecorino sardo is delicious in contexts where the romano could overpower, such as in pesto—the Ligurian pesto alla genovese is traditionally made with a mixture of Pecorino sardo and Parmigiano-Reggiano—or with fruit.'''),  # noqa: E501
    ('Italy', 'Raschera', 'Piedmont', '''It has an ivory white color inside with irregularly spaced small eyes, and a semi-hard rind which is red gray sometimes with yellow highlights. It has a savory and salty taste, similar to Muenster cheese, and can be moderately sharp if the cheese has been aged.'''),  # noqa: E501
    ('Poland', 'Bryndza Podhalańska', 'Podhale region', '''Polish variety of the soft cheese bryndza. It is prepared with sheep milk and was registered in the European Union's Register of protected designations of origin and protected geographical indications on June 11, 2007 as a Protected Designation of Origin (PDO).'''),  # noqa: E501
    ('Poland', 'Bundz', 'Podhale', '''A sheep milk cheese.'''),  # noqa: E501
    ('Poland', 'Koryciński', 'Podlaskie Voivodeship', '''Hard yellow cheese made from cow's milk. Named after the town of Korycin.'''),  # noqa: E501
    ('Poland', 'Królewski', 'Northwestern Masovia', '''Royal cheese; similar in taste and appearance to Swiss Emmental.'''),  # noqa: E501
    ('Poland', 'Oscypek', 'Tatra Mountains', '''Smoked sheep milk cheese, there is also a smaller form called redykołka, known as the 'younger sister' of oscypek.'''),  # noqa: E501
    ('Poland', 'Redykołka', 'Podhale', '''Sometimes known as the "younger sister" of Oscypek and the two are occasionally confused. The cheese is often made in the shape of animals, hearts, or decorative wreaths.''')  # noqa: E501
    ]


@pytest.fixture(scope='module')
def dbsession():
    ''' fixture for testing with database connection '''

    settings = {'sqlalchemy.url': 'sqlite:///:memory:'}
    engine = engine_from_config(settings, 'sqlalchemy.')
    session_factory = sessionmaker()
    session_factory.configure(bind=engine)
    Base.metadata.create_all(engine)

    session = session_factory()

    for country, name, region, description in cheeses:
        model = Cheese(
            country=country,
            name=name,
            region=region,
            description=description
            )
        session.add(model)
    session.flush()

    yield session

    Base.metadata.drop_all(engine)
