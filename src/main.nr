use dep::std::hash::poseidon;

// ---------- HELPERS ----------
fn abs_u128(x: u128, y: u128) -> u128 {
    if x >= y { x - y } else { y - x }
}

fn dist4_u128(a: [Field; 4], b: [Field; 4]) -> u128 {
    let a0 = a[0] as u128; let b0 = b[0] as u128;
    let a1 = a[1] as u128; let b1 = b[1] as u128;
    let a2 = a[2] as u128; let b2 = b[2] as u128;
    let a3 = a[3] as u128; let b3 = b[3] as u128;

    let d0 = abs_u128(a0, b0);
    let d1 = abs_u128(a1, b1);
    let d2 = abs_u128(a2, b2);
    let d3 = abs_u128(a3, b3);

    d0*d0 + d1*d1 + d2*d2 + d3*d3
}

fn features4(p: [Field; 5]) -> [Field; 4] {
    [p[0], p[1], p[2], p[3]]
}

fn label_u32(p: [Field; 5]) -> u32 {
    p[4] as u32
}

fn k_nearest_sum_label(
    pts: [[Field; 5]; 50],
    q: [Field; 4],
    k: u32
) -> u32 {
    // distance u u128 da bismo mogli da koristimo <
    let mut dists: [u128; 50] = [
        dist4_u128(features4(pts[0]), q),  dist4_u128(features4(pts[1]), q),
        dist4_u128(features4(pts[2]), q),  dist4_u128(features4(pts[3]), q),
        dist4_u128(features4(pts[4]), q),  dist4_u128(features4(pts[5]), q),
        dist4_u128(features4(pts[6]), q),  dist4_u128(features4(pts[7]), q),
        dist4_u128(features4(pts[8]), q),  dist4_u128(features4(pts[9]), q),
        dist4_u128(features4(pts[10]), q), dist4_u128(features4(pts[11]), q),
        dist4_u128(features4(pts[12]), q), dist4_u128(features4(pts[13]), q),
        dist4_u128(features4(pts[14]), q), dist4_u128(features4(pts[15]), q),
        dist4_u128(features4(pts[16]), q), dist4_u128(features4(pts[17]), q),
        dist4_u128(features4(pts[18]), q), dist4_u128(features4(pts[19]), q),
        dist4_u128(features4(pts[20]), q), dist4_u128(features4(pts[21]), q),
        dist4_u128(features4(pts[22]), q), dist4_u128(features4(pts[23]), q),
        dist4_u128(features4(pts[24]), q), dist4_u128(features4(pts[25]), q),
        dist4_u128(features4(pts[26]), q), dist4_u128(features4(pts[27]), q),
        dist4_u128(features4(pts[28]), q), dist4_u128(features4(pts[29]), q),
        dist4_u128(features4(pts[30]), q), dist4_u128(features4(pts[31]), q),
        dist4_u128(features4(pts[32]), q), dist4_u128(features4(pts[33]), q),
        dist4_u128(features4(pts[34]), q), dist4_u128(features4(pts[35]), q),
        dist4_u128(features4(pts[36]), q), dist4_u128(features4(pts[37]), q),
        dist4_u128(features4(pts[38]), q), dist4_u128(features4(pts[39]), q),
        dist4_u128(features4(pts[40]), q), dist4_u128(features4(pts[41]), q),
        dist4_u128(features4(pts[42]), q), dist4_u128(features4(pts[43]), q),
        dist4_u128(features4(pts[44]), q), dist4_u128(features4(pts[45]), q),
        dist4_u128(features4(pts[46]), q), dist4_u128(features4(pts[47]), q),
        dist4_u128(features4(pts[48]), q), dist4_u128(features4(pts[49]), q)
    ];

    let mut sum: u32 = 0;
    let inf: u128 = 1_000_000_000_000; // dovoljno veliko da "izbaci" element

    let max_k = 10; // maksimalan K koji dozvoljavamo

    for kk in 0..max_k {
        // nadji argmin
        let mut best_i = 0;
        let mut best_d = dists[0];

        for i in 1..50 {
            let di = dists[i];
            if di < best_d {
                best_d = di;
                best_i = i;
            }
        }

        // uzmi label samo ako je kk < k
        let take: u32 = if (kk as u32) < k { 1 } else { 0 };
        let lbl: u32 = label_u32(pts[best_i]);

        sum = sum + lbl * take;

        // "izbaci" vec izabrani najblizi (samo ako ga uzimamo)
        let new_val = if take == 1 { inf } else { dists[best_i] };
        dists[best_i] = new_val;
    }

    sum
}

fn majority_from_sum(sum: u32, k: u32) -> Field {
    let th: u32 = (k + 1) / 2; // ceil(k/2)
    if sum >= th { 1 } else { 0 }
}

// ---------- MAIN ----------
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
    public_inputs:[Field;7],
    salt: Field,
) -> pub Field{
    // commitment rekonstrukcija
    let rest:[[Field;5];49] = [
        p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12,p13,p14,p15,p16,p17,p18,p19,p20,
        p21,p22,p23,p24,p25,p26,p27,p28,p29,p30,p31,p32,p33,p34,p35,p36,p37,
        p38,p39,p40,p41,p42,p43,p44,p45,p46,p47,p48,p49,p50
    ];

    let mut h: Field = poseidon::bn254::hash_5(p1);
    for i in 0..49 {
        let n = rest[i];
        h = poseidon::bn254::hash_6([h, n[0], n[1], n[2], n[3], n[4]]);
    }
    assert(h == public_inputs[0]);

    // query + K +  ed
    let q = [public_inputs[1], public_inputs[2], public_inputs[3], public_inputs[4]];
    let k: u32 = public_inputs[5] as u32;

    let salt_commit = public_inputs[6];
    assert(poseidon::bn254::hash_1([salt]) == salt_commit);

    let pts: [[Field;5];50] = [
        p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,
        p11,p12,p13,p14,p15,p16,p17,p18,p19,p20,
        p21,p22,p23,p24,p25,p26,p27,p28,p29,p30,
        p31,p32,p33,p34,p35,p36,p37,p38,p39,p40,
        p41,p42,p43,p44,p45,p46,p47,p48,p49,p50
    ];

    let sum_u32 = k_nearest_sum_label(pts, q, k);
    let pred = majority_from_sum(sum_u32, k);
    let pred_commit = poseidon::bn254::hash_2([pred, salt]);
    pred_commit
}
