use dep::std::hash::poseidon;
use dep::std;

fn main(
    p1:[Field;5], p2:[Field;5], p3:[Field;5], p4:[Field;5], p5:[Field;5],
    p6:[Field;5], p7:[Field;5], p8:[Field;5], p9:[Field;5], p10:[Field;5],
    p11:[Field;5], p12:[Field;5], p13:[Field;5], p14:[Field;5], p15:[Field;5],
    p16:[Field;5], p17:[Field;5], p18:[Field;5], p19:[Field;5], p20:[Field;5],
    p21:[Field;5], p22:[Field;5], p23:[Field;5], p24:[Field;5], p25:[Field;5],
    p26:[Field;5], p27:[Field;5], p28:[Field;5], p29:[Field;5], p30:[Field;5],
    p31:[Field;5], p32:[Field;5], p33:[Field;5], p34:[Field;5], p35:[Field;5],
    p36:[Field;5], p37:[Field;5], p38:[Field;5], p39:[Field;5], p40:[Field;5],
    p41:[Field;5], p42:[Field;5], p43:[Field;5], p44:[Field;5], p45:[Field;5],
    p46:[Field;5], p47:[Field;5], p48:[Field;5], p49:[Field;5], p50:[Field;5],
    public_inputs:[Field;5]
) {
    let rest:[[Field;5];49] = [
        p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12,p13,p14,p15,p16,p17,p18,p19,p20,
        p21,p22,p23,p24,p25,p26,p27,p28,p29,p30,p31,p32,p33,p34,p35,p36,p37,
        p38,p39,p40,p41,p42,p43,p44,p45,p46,p47,p48,p49,p50
    ];

    let mut h:Field = poseidon::bn254::hash_5(p1);
    for i in 0..49 {
        let n = rest[i];
        h = poseidon::bn254::hash_6([h, n[0], n[1], n[2], n[3], n[4]]);
    }

    print(h);
}
