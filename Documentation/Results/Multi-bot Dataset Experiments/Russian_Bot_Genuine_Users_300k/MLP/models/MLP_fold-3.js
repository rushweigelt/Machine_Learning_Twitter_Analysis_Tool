var MLPClassifier = function(hidden, output, layers, weights, bias) {

    this.hidden = hidden.toUpperCase();
    this.output = output.toUpperCase();
    this.network = new Array(layers.length + 1);
    for (var i = 0, l = layers.length; i < l; i++) {
        this.network[i + 1] = new Array(layers[i]).fill(0.);
    }
    this.weights = weights;
    this.bias = bias;

    var compute = function(activation, v) {
        switch (activation) {
            case 'LOGISTIC':
                for (var i = 0, l = v.length; i < l; i++) {
                    v[i] = 1. / (1. + Math.exp(-v[i]));
                }
                break;
            case 'RELU':
                for (var i = 0, l = v.length; i < l; i++) {
                    v[i] = Math.max(0, v[i]);
                }
                break;
            case 'TANH':
                for (var i = 0, l = v.length; i < l; i++) {
                    v[i] = Math.tanh(v[i]);
                }
                break;
            case 'SOFTMAX':
                var max = Number.NEGATIVE_INFINITY;
                for (var i = 0, l = v.length; i < l; i++) {
                    if (v[i] > max) {
                        max = v[i];
                    }
                }
                for (var i = 0, l = v.length; i < l; i++) {
                    v[i] = Math.exp(v[i] - max);
                }
                var sum = 0.0;
                for (var i = 0, l = v.length; i < l; i++) {
                    sum += v[i];
                }
                for (var i = 0, l = v.length; i < l; i++) {
                    v[i] /= sum;
                }
                break;
        }
        return v;
    };

    this.predict = function(neurons) {
        this.network[0] = neurons;

        for (var i = 0; i < this.network.length - 1; i++) {
            for (var j = 0; j < this.network[i + 1].length; j++) {
                this.network[i + 1][j] = this.bias[i][j];
                for (var l = 0; l < this.network[i].length; l++) {
                    this.network[i + 1][j] += this.network[i][l] * this.weights[i][l][j];
                }
            }
            if ((i + 1) < (this.network.length - 1)) {
                this.network[i + 1] = compute(this.hidden, this.network[i + 1]);
            }
        }
        this.network[this.network.length - 1] = compute(this.output, this.network[this.network.length - 1]);

        if (this.network[this.network.length - 1].length == 1) {
            if (this.network[this.network.length - 1][0] > .5) {
                return 1;
            }
            return 0;
        } else {
            var classIdx = 0;
            for (var i = 0, l = this.network[this.network.length - 1].length; i < l; i++) {
                classIdx = this.network[this.network.length - 1][i] > this.network[this.network.length - 1][classIdx] ? i : classIdx;
            }
            return classIdx;
        }

    };

};

if (typeof process !== 'undefined' && typeof process.argv !== 'undefined') {
    if (process.argv.length - 2 === 8) {

        // Features:
        var features = process.argv.slice(2);

        // Parameters:
        const layers = [32, 32, 1];
        const weights = [[[1.3351606559991116, -0.9369292681734868, -0.35730509131083854, 0.9553041221600121, 1.3687809959293245, 1.1394421441501843, 2.010977860397917, -0.5100079892306564, 0.16344730216952044, -0.6001973745687285, 1.3151586115558145, 3.3447353432381632, -1.3172172459104246, 2.414811904001572, -0.8744150691939461, -1.3993324195836263, 1.0730435454318792, -0.7552608945041618, -0.5148794794092573, -0.9706119663023163, 1.5248772543894322, 0.476782268832801, 0.39895870547638046, -1.0502574760257846, 0.8524564712033508, 0.5074920093152786, 0.5402691632513095, -1.2231969192077639, 0.39001993390775486, 1.208922616304335, -0.350691760912559, -0.8294275822893141], [0.17119464290284925, -0.4889008663705519, 1.2255112833991917, 0.2717280238802361, -0.484238226950748, -0.5983207387939581, 0.48846633902795517, 0.5048445926112252, -1.541569693833532, -0.6231645133009382, -0.46481381222862206, -0.14651482268032678, 0.4895084854540101, 0.5338861926195614, -0.5789687614102016, 0.2955183418007793, -0.20228628545195643, 0.7805035613167135, 0.8766233347663629, -0.33381426734377406, -0.44323231711375427, -0.6171481596670113, -0.017536750909964684, 0.2727644346530565, 0.03530512023152641, 0.689963893741293, -0.34862765333467477, 0.3168689830626993, 0.9316470881194667, 1.2781382199343905, 0.46750361347947494, 0.756775629236764], [0.9085897740783154, 0.07807730300864625, 1.1551599994960378, -1.2860355054944215, -0.20010981557041072, 1.021010158494805, -1.1008975254419828, -1.280548835857567, 0.3203042997621341, 0.3887956053521974, -0.21233225153501134, 0.616446982890675, 0.5269195109336731, -0.378506971855187, 0.6488675865895259, -0.6792428070748622, 0.43722340522370545, -0.49036977560702755, -1.0971725986342784, 0.9030472444785111, 0.5065048438090212, 0.7270419787039499, -0.18355519512332355, -1.2565709678170631, -1.159396436265315, -1.4411248489549457, 0.21058551908561401, 0.6233248887896211, -0.19314990058769624, 1.0898291939860572, 1.165612673943767, 1.199712710586263], [1.1947678743056143, 1.8838526708129657, 1.028054696924193, 2.342512704480318, -0.5927159051319214, -2.5884507148211453, -1.335495788412257, -0.10332069434560759, 1.0314346892860653, -0.37410750547875776, 0.45827197092510347, 0.6007651989053348, 1.1860196913345225, 0.0682457595803811, -3.027169164941738, 2.8325891578909457, 0.6930942810380756, 0.3870558145685965, -1.8288407974650072, -4.523696672653122, -4.028162854843973, -3.3622157788583187, -0.028596473038568163, -0.15287948535412305, 2.766767840726399, 2.354159761978818, 0.15340658999992146, 1.8741550449795052, -0.4800146265954889, 0.6583415478875888, 1.1546794711432797, 2.4617259340844715], [-2.1850177843483327, 1.6276916611967307, -0.2121591329897914, 0.660932454663438, 2.0545667460160697, -1.7405416572771997, 1.8034007215780872, 2.2854826961589136, 0.3763651138307815, -0.8676300948552589, 1.995809962862753, -1.0910624410497893, -0.5010635650928972, 2.3110319477365957, -1.782901223296779, 1.3437995257765538, -1.3856254907831498, 0.14564850420402195, 0.8019896058613937, -0.41034174318161293, -2.0682002553397294, -1.3865029480015458, 0.31382154841094967, 1.7399633780524648, 1.4517472548805248, 1.4120024323875162, 0.5679277329631689, -0.9827716034253452, 1.6812074987031582, -0.29392194181627046, -1.0122596362642735, -2.3675613136393143], [0.02668811919070912, -0.8473386520423514, 0.001893148286771423, -0.5681044769559457, -0.005699554523326271, -0.3315832794208486, -0.036813136663111874, -0.0027625997219824514, 0.03256962747166047, 0.38909432513209774, -0.10280729752852118, -0.04947937983002082, 0.19518132955121786, 0.010734280947564876, 0.07723648414466008, 0.30076071455809433, 0.4990805822114963, 0.19824817930715216, -0.020058943662655263, 0.004410157141229684, -0.029919626714451638, -0.0008922945994737082, -0.40261911327213235, -0.00046169288067036886, 0.5215562830559816, -0.6815188125441094, -0.006805505281419577, -0.0026663874118531155, 0.5376360322128324, 0.12291517952948906, -0.16109903178095739, -0.14263593058210128], [-0.39076247088456134, -0.17050435351733056, 0.15920460211560328, -0.7065288361436333, 0.614577473536677, -0.1854999308706362, 0.00043966441250256947, 0.5483828488619226, 0.35909915991173363, -0.27922753324378374, 0.7591500388973806, -0.017622668119744826, 0.004700641967790596, 0.34741422287225304, 0.0214781300433644, 0.12492625776051922, 0.5790305724846287, -0.6588085620421898, 0.055651390601650176, 0.00775756232174426, 0.01507680516639115, 0.2061116680003915, -0.4390980618329434, 0.69918828377433, -0.32842128264992587, -0.07758034206082766, 0.12926654561378198, 0.5447320335586326, -0.0011422075554077546, 0.0809704694139914, 0.4196794282615356, 0.03053515622176928], [0.15973423754872196, 0.058166882512031455, 0.11865070359295382, 0.31217515129639384, -0.35338125002780546, -0.23749963241697394, 0.488482372719444, 0.3185389248685417, 0.96611824257265, 0.4698193371986386, -0.39231431371046543, 0.6093250709562515, -0.21611196386900805, -0.008493036349213653, -0.39300685319577805, -0.2487785407322256, 0.11130251764314357, 0.6211999850611772, -0.721799158837242, -0.005684546864109928, -0.012407754810526687, -0.38216502050476964, -0.5862495433155005, -0.33547129143452076, -0.08895711505163939, -0.6498404435062819, 0.0526929740081273, 0.42164128986946703, 0.6283378806644622, -0.004681124489683558, -0.5871780738790738, 0.013475283389135392]], [[-0.4432869470962921, 0.6743477298398053, 0.17354314035243204, 0.12786626050130026, -0.04752850047597506, -0.33522564313502007, 0.10084834703643084, -0.06393046693478646, -0.8387284958885566, 0.23924671818300544, 0.12287650953910599, -0.6621078259204054, 0.34569125311672094, 2.355432107e-315, 1.999950976e-315, -0.707339846834559, -1.0018687404264335, 0.27850612721335005, 0.5160555935393359, 0.3773801340202163, -0.5426237214824869, -0.22294745937873872, 0.7484325872754577, 0.5630589190286744, 0.32570684222435387, 1.0710765895232723, -0.4106068529139106, -0.504837121517149, 0.315314777257855, -2.94493632e-315, -0.34887380195403794, -1.20319659e-315], [0.051847799887655276, -0.4041652468396626, -0.08897180092780423, -0.7108398485488083, 0.2719769006775517, 0.13727150542274627, -0.09334354403532227, 0.29832215698603726, 0.5094984469733175, -0.8236780049657509, 0.8516810737227549, -0.35543509030517645, 0.48684325277600615, 1.687634823e-315, 8.15812187e-316, 0.540600494574205, -0.2246069365632483, 0.40508670485339193, 0.9432038905654841, -0.012570272015028841, -0.1753037279725241, 0.1246553409109641, -0.3288568858787077, 0.9833609574104818, 0.5762578352882469, -0.6559210599644535, -0.007718580547457307, 0.5692314178642723, -0.14475565830556306, -1.191834834e-315, 0.6232475691559188, 3.014652164e-315], [-1.0941741221265777, -0.05417334930498476, 0.569600266931846, 0.7025492014208916, -1.1892441001797645, -0.328762889843164, 1.011800100056409, -2.3736261513650025, 0.031829351019193236, 0.2719745359403138, -0.31704459714114475, -0.6268948728393748, 0.6164789807192501, 8.52926913e-316, -2.12178693e-315, -0.0039032337114992175, -0.21229789537340168, -0.03942720111943553, 0.5940836497778514, 0.5569973861999767, -0.6772512806757904, 1.0819591995313615, 1.0771029125968241, 0.6682629587735615, -1.3768968090367559e-273, -0.7402677012647535, 0.015306793359179139, -0.6805715918300623, 0.29461000392501785, -3.01616251e-315, -0.8657158155925261, 3.05924482e-315], [-1.1505284988177813, -0.02979349716870157, 0.1471159246344936, -0.43407700356633905, 0.1434406043059258, 0.33364432771941926, -0.2862208056657299, 0.8631586203447432, 0.025968459210807773, 0.11422831128113106, 0.3057605238170027, -0.5331723952045616, 0.0374749933364859, -2.556809e-316, 1.974672853e-315, 0.4802061440944431, 0.8301057688314467, 0.1648206471818836, -0.1430771527228102, -0.19078068164252854, 0.5745608828525987, -0.06944041564550432, -0.33019722327033707, -0.4243461438506759, -0.7355237740587615, -0.6462532179535392, 0.22068727276781355, 1.2956668586163063, 0.14193969954141888, 9.889252e-317, 1.3884499336151004, -1.94236208e-315], [0.6889461468709451, -0.27387360549351947, -2.2691013846929415, -0.4429717656904704, 0.4542374778314848, 1.089803355357418, -0.09756865388154122, 0.32659147302847236, 0.40112362192445006, -2.249052485238156, 0.9035656862160891, 0.7746296279516118, -0.624466229707333, -2.76061571e-315, 3.90126704e-316, 0.5902352450693698, 0.501075621289901, -2.1771655429463, -0.9598444165521526, -0.19726693384582883, 0.46791419561457637, 0.11631791275563094, -0.005712873328143542, -1.1615067339658436, -0.021985165931620775, -0.6423227478612097, 0.38005277910269575, 0.5960336358271647, -0.31507061962712546, -2.229373175e-315, 0.1787051112041552, -1.451277924e-315], [-0.15527590403739866, 0.20045273502570768, -0.5552714102959577, -0.1535648462998693, 0.27821556578054507, 0.2643446495496655, -0.02067593716333464, 0.3169570843640169, 0.2531618434359958, -2.5990983526508374e-11, 0.36368967932238244, -0.527062499352469, -1.3951677017942012, -3.206915355e-315, 2.112317536e-315, -0.19762112237382465, -0.9087698260424728, 0.2343900585907985, -1.828673015762588, 0.23761821828032512, -0.854204956753132, 0.6235570322440219, 0.4300341706110571, -2.0977196790679433, 0.5119328774791282, 0.20042265628809453, -0.702536248312773, 0.18238443932536214, 0.04414877972037544, 3.257391e-316, -0.021670260956115954, -6.8706372e-316], [0.6805496020413121, -0.20626265370849733, -1.200458462658522, -0.7029703524982988, 0.5492757862222681, 0.714915895409468, -1.539010108396052, 0.481242974204472, 0.9940569785183873, 0.5554286749984514, 0.5426008097826515, 0.3451948667763813, -0.6126330061215778, 7.34561536e-316, 4.6982822e-316, 0.7494861023575333, 0.9562963849892901, -0.7468997402256966, -0.6453841249429745, -0.281765589483437, 0.9403083090176615, -0.22617952355243087, -0.6609095593580364, -0.874964560199897, -1.701258227223981, -0.6082468326137712, -0.3155264300414341, 1.1164508760323617, -0.4622281428587779, 9.75602923e-316, 1.1856298980602566, 3.02782267e-315], [0.3638818017056063, -1.7349868738895686, 0.7142138514278507, -0.3727681637008162, 0.57990171434634, 0.38184000858068196, -0.6348120350811646, 1.327863633998518, 0.15975266116928655, 0.1605444108579426, 0.43808471202398946, 1.0305547880950054, 0.41262448110526745, -2.36301885e-316, -1.844002213e-315, 1.0155413395341233, 1.0803810084663357, -0.42170012320837563, 0.41416838936538736, 0.04768207537381192, 0.8698688178124011, 0.053165115849274254, -0.9441395066739855, 0.41954351292143294, -0.4058006897759258, -1.2987963515697958, 0.6944577879160226, 0.597158440319847, -0.5379779517938045, -2.548406634e-315, 0.6305278400210287, 2.95902357e-315], [0.8812427708647667, -0.05979103031340748, 0.23765008426600245, 0.030205874441501714, 0.3500869135088192, -0.06785410641582401, -0.4799516489376006, -0.8416819139017563, 0.3467978221702218, -0.4617714236673806, 0.029529241876651482, 0.22712075775319404, -3.3071356093157487, 1.555692587e-315, 2.00216113e-315, 0.0766499974967748, 0.36516186027101205, -0.0630256194856341, -5.349033696661869, 0.41832371338111946, 0.3725149029246711, 0.6055222338529916, -0.48132317749391224, -6.0758875312889655, 0.43006284549840157, -0.155552241101427, 0.07850678999469869, -0.3056765307713539, 0.11885758066849073, 9.70459443e-316, -0.37899948540038303, -1.218137995e-315], [-0.13441227186097626, 0.03742333990194552, 0.476106105108535, -0.0516270376783631, 0.2258170147333911, 0.23007023022719125, 0.12043169287555434, 0.0977787798862249, 0.28689776620779445, -3.2300367121945373, -0.14254343040111053, -0.5710842950917085, -0.5013345504695358, 2.902061876e-315, -1.703000077e-315, 0.6541624507283565, 0.09753350145985125, -2.21419611302077, -0.06128857040384759, 0.316304406673598, -0.06574029683023631, 0.7195958209026727, -0.019030797838893325, -0.17443666273352262, -0.2357849292624046, 0.3185768089857952, 0.6189186985839336, 0.4000970806741727, 0.215017193370423, -4.6510578e-316, 0.3401791852477934, -1.60568736e-315], [1.1068129447571964, 0.5700541864522382, -2.290095777008238, 0.41208569645684245, 0.05510482757832494, -0.053051668605817635, 0.7139680824868079, -0.7764526295818279, 0.8112093684695306, -1.2445433154072343, 0.36578077914902946, 1.0241347034246844, -1.6099003717049007, -2.100480435e-315, 8.985533e-316, -0.5044729794642077, 0.867366275581672, 1.1883120162410148, -0.7065251024445082, -0.2083460405846452, 0.47848812441283295, 0.7128263808539622, 0.5387137363163228, -1.0610756669517447, -0.7353580230841716, 0.5412278513310758, 0.4969546874671185, -1.2385467533280985, 0.476031718244248, 1.953361173e-315, -1.117362932158788, 3.13789811e-315], [-1.2224866968822672, 0.8808223992262568, 0.19649669199038206, 1.0335819069146088, -0.3157710244266904, -0.7462917705902044, 0.8843341350614209, 0.5398839133430016, 0.11701095543239008, -0.7877875509318343, -0.5642578330711616, -0.024884425378308834, 1.0594821795874014, 3.179602166e-315, 3.14225706e-316, -1.5676880687795818, -1.6864479009523896, 1.761348334706458, 0.8926590031384877, -1.2926860146618075, -1.8538323865688906, -0.9723746278298568, 0.5689414425785502, 1.0659248654620128, 0.586468411464866, 0.7227520558492326, -1.296657440858446, 0.5302120282672413, 0.7915073042979214, -1.629991512e-315, 0.41182429576146373, -1.15309803e-315], [0.13845673393529395, 0.6869287235693962, -0.028873059219964685, 0.4159228509177986, 0.8484639921984282, -0.7244437426650164, 0.7760871572507004, -0.16105393386395017, -0.4764675684244654, -0.4702332948615701, -1.6535402435376938, -0.7782059156560746, 0.4160200644355221, -5.68711776e-316, -2.094409544e-315, -0.3994458435896184, -0.5883232836772173, -0.07750766135105423, 0.2911973735257912, 0.4096718318210354, -0.194539645359049, 0.5249541104646519, 0.4241990139532927, -0.053601417747337274, 0.4701349369476638, 0.4877881750015485, 0.7472755300236306, 0.5167187112958217, -0.5812425050850785, 5.92512667e-316, 0.5164442701501127, -3.162412634e-315], [1.5600695562517803, -1.5468733441463565, -0.8225273212000084, -0.47842970278534075, 0.7169553838344414, 0.5759955272740397, -1.2888450822359834, -0.7186221597746815, -0.5259250489808945, 0.623682761778077, 1.3162802168912762, 0.30872094607182676, -0.3736675616714291, -3.5573716e-316, 3.266437454e-315, 0.02836383220832393, 0.013050165737392759, 0.9700080480013497, 0.0894758747660787, -1.3146372886555744, -0.10871787217792145, -1.792675489041515, -1.4256064928553087, -0.14576533420692256, -4.845716021641448, -1.056528514644898, -0.7142350324298846, -1.0765094455454196, -0.42197506328286083, 1.192056437e-315, -1.4833192530535884, -8.66016006e-316], [-1.9461895006380738, 0.4214322941732742, 0.31323766464951464, 0.7988742754410337, -0.4817809691819932, -0.4952157618120152, 0.24587918957548174, -0.20840916521789432, 0.7903433999749909, -2.66453001e-315, -0.3328217025413668, -0.26323033407965624, 0.5534834211774312, 1.533122334e-315, -1.047744813e-315, 0.06743777956867308, -0.6262828177732872, 0.21244190291663073, 0.2173712656378982, 0.16709464210764252, -0.4943238007230847, 1.0534784863656843, 0.23838887287660826, 0.3270915824011969, 0.30379673264869794, 0.37868186493498157, 0.7638029979502415, -0.0035881556060697786, 0.1103053622421759, -3.08374764e-316, -0.0752566686893376, 3.8778076e-316], [-1.5311684567831825, -0.9548265650512422, 0.5066092229011098, -0.9390626560411427, 0.5998348826441774, 0.19076922043088176, 0.17876396358904964, 0.6212109401107788, -0.2876646822253668, -0.28414668539009436, -0.3596441973883493, 0.3277202891898838, 0.7620280508025185, -4.8932034e-316, 1.585183943e-315, 0.37722630806727653, 0.26505643357978603, -0.44840097804110235, 0.3765211666995812, 0.14052826323661718, 0.4915652457038756, -0.06408158883708683, -0.04555647837188001, 0.6967772361056436, 0.6197378005069958, -0.7334825151156515, -0.0767889073527595, 0.4455046371888586, -0.5816794607977394, 1.666038883e-315, 0.4415575804915627, -3.360758207e-315], [-0.8267061153444073, 1.201921090545935, -0.1113076145682195, 0.8965789169850936, -0.5702533211357588, -0.552438980761874, 0.9820035967170918, 0.07647198545355621, 0.7220927481782327, 0.36418651072574865, -0.8657208859566112, 0.33560641400082447, -0.3322023192900946, 3.28766575e-315, 2.026625106e-315, -0.6632450776853024, -0.20786934331486137, 1.3869513433740512, -0.1636638305881375, 0.36887865927839775, -0.3585068694342044, -0.517828453555747, 0.7068946346947358, -0.001520193843986313, 1.4014502465068865, 1.5100271141909503, -0.22470166398542454, -0.055800684261820055, 0.5182245330392928, -1.592671053e-315, -0.5121006119414125, 3.14329505e-316], [-0.016725147025244105, 0.1763167612876938, 0.308417214880557, 0.29666249910569353, -0.09893105115191715, 0.07074272956613989, 0.14883971757084458, 0.017245068986923465, 0.03155122868332034, -0.3133059428693231, -0.039942931898614226, 0.30050884380088244, 0.03250569216993104, 2.27567358e-315, -2.5732719e-315, 0.20717879174633988, 0.6888755272662531, -0.32435590698502426, 0.1534615339816552, 0.17506717648166842, 0.6830838346454458, 0.6881714759025438, 0.2770982238292279, 0.5422741911778504, -0.048066786597890224, 0.08951902682757927, 0.6673411824766221, -0.1141974151704237, 0.3809565481537908, 1.50454961e-315, 0.21483179756074225, 5.74204927e-316], [-0.22552662433955126, 1.0156584318265764, -0.09716677864948312, 0.8791118740547073, -0.8081549813455704, -0.5692734329606135, 0.20011356765611835, -0.08315893598048811, -1.434206100690879, 0.0021842116985093967, -0.4631697680317955, -0.26497590500613666, -0.01299195293307667, -3.8659008e-316, 2.766914374e-315, -0.07890334288772331, 0.5660193537939907, 0.47297271569269916, 0.1209423215531767, -0.0222148846665091, 0.5589459779894232, -1.0653212592151262, 0.33525010905190755, 0.3172397388514874, 0.43300913387093587, 1.0416671054416515, -1.2506002351187617, -0.2508127167244237, 0.7086988153260867, -1.12536072e-315, 0.17333797388523894, 3.5570974e-316], [-3.5898969770307887, 0.5828305467996614, 1.1408721481362587, 0.885634555194418, -0.7211612395474618, -4.634118829675727, 0.7243205515355944, 0.6502896630875503, 1.048243160792316, 2.9949086e-316, -4.674141075740877, -0.24718459631585118, 1.6336926884788308, -3.9895056e-316, -2.29308304e-315, -0.52832852012932, -4.236115242065748, -1.1643840048429377, 2.7367339859342206, 1.1414032155435812, -4.240511398117086, 0.23626964147474863, 0.5059035600713155, 2.9232452433368614, 0.7917827058449805, 1.0085986470983133, 0.45017825537905226, -0.8834636666669028, 1.102894853243697, 3.00130813e-315, -0.7000956121449645, -7.42452303e-316], [0.4746792632450351, 0.49893855686012495, -1.2603329437133028, 0.08479066196659697, 0.28450138379528783, 0.28748147909210825, 0.2844012264895023, -0.40929941998539715, -0.20564154168571933, -8.411696002390201, 0.31073616344406974, -0.6101876589845684, -0.6056957025845205, 6.78379607e-316, 1.30485069e-315, -0.7274278095243074, -1.6716365503272121, 0.015225576644487449, 0.24722894373157428, 0.10402695306711013, -1.3846889455454439, -0.7742867699008498, 0.7821982102560746, 0.8214255026782546, 1.005206326805849, 0.9527072555302577, -0.7137161253041125, -0.4763080530899234, -0.14412018316448214, -2.15815864e-315, -0.4786692989334554, 7.403669e-317], [-0.0833332210886853, 0.18765180800456746, -0.30978337867870215, 0.4772613537292894, -0.24678023139418584, -0.01536638643195646, 0.18203868469207954, -0.20856464814572617, 0.701437875059881, 4.2587393980407826e-13, -0.18217859610317672, -0.37531376780677517, -0.13883580131030132, 1.4850053e-315, 2.874907376e-315, -0.2102694468425594, -0.48807155697405585, 0.06132695841986756, -0.18679071999200264, -0.24340747366317936, -0.3448551552349909, -0.20423558871684894, -0.024989406438998402, -0.41915243776736016, -0.5492877615287167, 0.22621358787180057, 0.18196986691738645, -0.2287960325912282, 0.21244403462152642, 1.44468081e-315, 0.02477390341669962, 1.78975676e-315], [0.11341907345360029, 0.3320041691365779, -1.1270323097066892, 0.5347232758950534, 0.2932507275533688, 0.18360575019215258, -0.018718538622427394, 0.4428780396070801, -0.3427349908019591, 0.7705508725677492, -0.060667547795313394, -0.5077856514924711, -0.7734558112572876, -1.750980343e-315, 1.341199733e-315, 0.08911594828309174, 0.35003826022512785, 0.08179105916043335, -0.5926736637264862, -0.22491265638429872, 0.015126896002431256, -1.3552122131270334, 0.20402388120798765, -0.5895326166704526, -0.33061492357342925, 0.30829257631772217, -0.5743236300134461, 0.4658899016888166, -0.0071988181725894575, 8.712545e-316, 0.646694213757179, -7.23412954e-316], [1.4914998234145547, -1.189238269702319, 0.5295127801188333, -0.48873988168924004, 0.6524863385916643, 0.8346590452322338, -0.014175290347912175, 1.5974657497491591, -0.12715655055511174, -0.6336857039272066, 0.6815007811732969, 1.0089381430155606, 0.4151376075589419, 1.826680306e-315, 2.89705725e-315, 0.2802021711063065, 0.7368038546670215, 0.08209578059232898, -0.4462850718233912, -0.48147137742714136, 0.8179370386326533, -0.25751654495326054, -0.9182395819503144, -0.5194703712857621, -0.3966516808304005, -1.2145848517772249, -0.11631196468403825, 0.5709227464316462, -1.7589809749724508, -2.04504047e-316, 0.5456961625020817, 1.723854395e-315], [-0.2500297592704272, -0.5212617054524138, -0.29660595208012586, -1.2892722272790147, 0.5137674481509428, 0.7021007431241914, -0.14040117348117742, 0.7679067920949656, -0.7373040043352338, -0.13417674310862274, 0.7222779172264577, -0.42250479277936853, -0.21486040811343127, -2.62026736e-315, 2.143891177e-315, 0.2665436186876818, 0.4045467336500484, 0.12231004753989438, -0.0679569857061306, 0.1329643220542978, 0.13863854499659267, -0.807718037810848, -0.06442506070346204, -0.3148548472168977, -1.09127643768446, -0.2939599807041101, 0.9307065567434836, 0.6286601693209679, -0.6279060357386804, 1.1990082e-315, 0.650542796849529, -1.98627771e-315], [0.851844464754058, 0.1310500390217769, 0.08291963591501017, 0.8124117270662922, 0.006545656895267064, -0.009076378891598022, -0.2529219895966635, 0.4620506997429661, -2.646542924491807, -0.23879320147159833, 0.4547282763189498, 0.3372794741924112, 0.44845573032843783, -1.08826136e-315, -2.034106717e-315, 0.3695485513765443, 0.5399684920084189, 0.42281231409300485, 0.3591375539657631, -1.1448298139992046, 0.6588609143443723, 0.0849230117890995, -0.5385687418128156, 0.40098810631854503, -0.18012219716856256, 0.32659068616518727, 0.5621814597534133, 0.5351967773545174, 0.05012493368230079, 3.351677913e-315, 0.5038318989330564, 2.039145055e-315], [1.2154919778939814, -1.0815146458203597, 2.44399379e-315, -0.9599454771914303, 1.1301582964229338, 0.9224520379058333, -0.040834150746236766, 1.4030822014612527, -0.2879589855433424, -2.213241205e-315, 1.1513142810482613, 0.3510781850700915, -5.63364277e-316, -8.3785407e-316, 1.409234795e-315, -5.200594647126916e-131, 6.218409532638841e-51, -1.4093337567563722, 4.288678379195731e-233, 3.983836567e-315, -5.367444117198382e-97, -2.7853301703936083e-148, -0.8858683604861817, 1.903694883e-315, -2.43096781e-315, -1.160452346572979, 9.103993539210384e-131, 0.27964169142755774, -1.336401241997037, -4.04071213e-316, -0.034287449612552076, -9.94549684e-316], [-0.18259202178812292, 0.0716215608223575, 0.6939730818012596, 0.508113209009534, -0.55268932891964, -0.25833043396023037, 0.7869794355646208, -0.46837956983467904, -0.6591232717632699, 0.06745876993201894, -0.4596080776834225, -0.4952857083442889, 0.37820264123272535, -4.0733519e-316, 1.262571354e-315, -0.1493225631150559, -0.23394728957025213, -0.41994758918545977, 0.5863107934081131, 0.24282116346786115, -0.2234923367225079, 0.8149084295462514, 0.2911307945953667, 0.6337945351756132, 0.033029657383940765, -0.14271021432280853, 0.5864387407050526, -0.5263557410798066, 0.20604944439151887, -3.14405619e-315, -0.5848296707723046, -2.837918e-316], [0.5422820604768842, -0.4085162400862064, -0.16853198060393543, -0.7727787758454309, 0.15967143279325066, 0.8226141373333676, -0.6464128516411265, 0.4042568939470628, 1.1126973135581424, 0.506815514826185, 0.5108778680049244, 0.6383039185362896, -0.32178253939793205, -6.93026756e-316, 2.06735826e-315, 0.09580168721798889, -0.17604616011632454, -0.7501256703600877, -0.04738105661843159, 0.5852078764836797, -0.14225312314581207, 0.30467969446364435, -0.19516257413769153, -0.15389152199351389, -2.887445446055225, -1.5507674148049313, 0.5313182438987605, -0.0855683074813019, 0.088814809644755, 2.51434444e-316, -0.019582449523341455, -2.49306208e-315], [-0.7980977754911155, -0.4551689125476609, -0.3898098960386255, 0.5320615792837777, -1.6879258044223073, -0.041891311666679254, 0.4910130341793007, -2.554185422995427, -1.459043222797816, 1.085687154727565, 0.004081701964750495, -0.6590971260591042, 0.3530593743183205, 3.46187485e-316, 2.005716346e-315, 0.13842012621708058, -0.26516366222166055, 0.3141631655001289, 0.27342943780405715, 0.23538322373794862, 0.030331002830189604, -0.2932520482627458, 0.10258959117572089, 0.5765965937902144, -6.4033334e-317, 0.36446603326541904, -0.659234773473038, -0.6402507007474995, 0.1008445964942446, 3.31927233e-315, -0.9955916063488549, -1.17755124e-315], [-0.22729960455125617, 2.3469082871189157, 0.07479016976727482, 0.38414930873534875, -0.08101160854210394, -0.6849549068034921, 0.253350512350225, 0.487903510781677, -0.46781690523213965, 0.108070020033109, -0.5940345498202642, -1.2465135069775106, 0.0756878694548506, -1.046998675e-315, 4.57782626e-316, -0.14714913121267614, -0.3956071500655284, 0.01730335386949547, 0.12137411730165779, 0.1653474729932013, -0.030486833607705845, -0.6932009330198526, 0.47999474233929434, 0.1574048257038405, -1.9662845658394092, 2.127365276635384, -0.4263962766109169, -0.11135053358063988, 0.28124077203947756, 5.73595625e-316, -0.07052996487807447, 3.2826625e-316], [-0.24228145892770744, -1.8516275031513485, 0.6435314114478876, 0.2704441732935908, 0.5026515288343584, -0.5511516196718749, 0.42637157625853506, -0.027250619341413772, -0.16466051078983893, 0.14911378165734604, -0.797657585216471, 0.3875119591260631, 0.14042018693759295, -1.19456952e-315, 2.94380528e-315, -0.30366087728405516, -0.09320810777840792, 0.07664035940794767, 0.5622203004220705, 0.48351194750642146, -0.5867747941808088, 1.0566018856593307, 0.7166745132300921, 0.5193287726137806, -0.6357537573305125, -1.0162184482986516, 0.45483973710635794, -0.10071797343671089, 0.014739102598680906, -1.415260583e-315, -0.3283021855454566, -1.6863307e-315]], [[-4.466729678907969], [1.8586221878937583], [1.6181936844653233], [1.986284032111458], [-1.6117950677143027], [-2.0500380585993305], [1.5062045013467502], [-2.1450745026318963], [3.160174935727581], [-2.289342683962846], [-2.5824734529823274], [-2.212606145925764], [1.6687139650788954], [-1.34977316e-316], [-2.53074163e-315], [-1.5203553879610645], [-3.041070573436068], [2.6975956616317944], [2.2982838819644065], [1.4031826165308061], [-3.1768379837696004], [2.4746260363328476], [1.7350379618136493], [1.9779222702470136], [3.3551770613415512], [1.8354965651756192], [2.6546981916829], [-1.417909566257701], [1.0643129364243284], [5.65921264e-316], [-1.0743402588202757], [1.02968855e-315]]];
        const bias = [[0.24827141364825123, -0.4159588963087183, -0.6369071597699182, -0.1341499556405217, 0.16501362371546746, -0.04695842106825606, -0.1486279536151515, 0.373279732760417, 0.008957265672242707, -0.1621909848329007, 0.04270322191584422, -0.2412452588844746, -0.3068453603422429, 0.16865017412556232, -0.03139026102807534, 0.1969975136040795, -0.41925186061857056, 0.3509347602504207, 0.232485633036619, -0.5776377184057592, 0.26493864166067727, 0.2135132080988647, 0.35643163166806774, -0.18530547491190968, 0.4835819048817171, 0.08393232173138994, -1.5705462524932898, 0.21493214739297353, -0.20732302229864052, -0.7034246747936982, -0.251956564840731, 0.015812666331907272], [0.14036519949306658, 0.10449392296868455, 0.301659794936613, 0.26330795092466164, 0.21533712143942102, 0.1730428843868551, 0.5604422691816647, 0.3496388299464819, -0.799498680639775, -1.5208056641735175, 0.21207591558449587, 0.2279314925728452, 0.48060290912933246, -0.1569338666670621, -0.03066529013393316, 0.45117336636644245, 0.656689640480648, -0.052502559035567935, 0.3824531892686657, 0.22752652257452605, 0.7761028836081555, -0.20670407827012902, 0.602524932240725, 0.26312731916965176, 0.012571522561319565, 0.2790040386660799, -0.43334010204090806, 0.41523926679433226, 0.4654293130798058, -0.26555678732060845, 0.39251083923847613, -0.18575907285475113], [0.26183409729349066]];

        // Prediction:
        var clf = new MLPClassifier('relu', 'logistic', layers, weights, bias);
        var prediction = clf.predict(features);
        console.log(prediction);

    }
}