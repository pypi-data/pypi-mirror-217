
from pymbs import api
from pymbs.tranche import IndexRate, Tranche

LIBOR = IndexRate("LIBOR", "BBA15", 1.31)


# Begin Group 3
COLL_3 = Tranche(
    "COLL_3", 172872340, 5.5, 3, 14, "COLLAT", "FIX",
    "2003-05-01", "2003-06-15"
)

PSEUDO_1 = COLL_3.new_child_tranche(
    "PSEUDO_1", 165500000, 5.5, 3, 14, "PSEUDO", "FIX",
    "2003-05-01", "2003-06-15"
)

AB = PSEUDO_1.new_child_tranche(
    "AB", 1000000000, 4.25, 3, 14, "SEQ", "FIX",
    "2003-05-01", "2003-06-15"
)

PSEUDO_2 = PSEUDO_1.new_child_tranche(
    "PSEUDO_2", 62500000, 7.5, 3, 14, "PSEUDO", "FIX",
    "2003-05-01", "2003-06-15"
)

FB = PSEUDO_2.new_child_tranche(
    "FB", 62500000, 1.71, 3, 0, "SEQ", "FLT",
    "2003-05-15", "2003-06-15", floater_formula="LIBOR + 0.4",
    floater_cap=7.5, floater_floor=0.4
)

SB = PSEUDO_2.new_child_tranche(
    "SB", 62500000, 5.79, 3, 0, "SEQ", "INV/IO",
    "2003-05-15", "2003-06-15", floater_formula="7.1 - LIBOR",
    floater_cap=7.1, floater_floor=0, notional_with=[FB]
)

Z = COLL_3.new_child_tranche(
    "Z", 10372340, 5.5, 3, 14, "SEQ", "FIX/Z",
    "2003-05-01", "2003-06-15"
)

waterfall = [
    "pay_accrue(Z_ACRRUAL, Z)",
    "V3 = Z_ACRRUAL + COLL_3",
    "pay_sequential(V3, [PSEUDO_1, Z])",
    "pay_pro_rata(PSEUDO_1, AB, PSEUDO_2)"
    "pay_sequential(PSEUDO_2, FB)"
]

assumed_collat = api.load_assumed_collat()
group_3_cf = api.run_collat_cf(3, repline_num=0)

# api.pay_waterfall(waterfall)
