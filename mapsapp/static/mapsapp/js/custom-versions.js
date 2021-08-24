$(function () {initCustomVersions();});
function initCustomVersions() {
    $('.x256TechButton').unbind().click(function (event) {
        let url = $(event.target).closest('.btn-group').find('.map-download').attr('href');
        let mapName = $(event.target).closest('.map-info').find('.card-title a').text();
        let filename = getFilename(url);
        $.ajax({
            url: url,
            beforeSend: function (xhr) {
                xhr.overrideMimeType("text/plain; charset=x-user-defined");
            }
        }).done(function (data) {
            if (data.startsWith('PK\x03\x04')) {
                const items = filename.split('@', 2);
                filename = items.length === 2 ? 'ZR@256x_' + items[1] : 'ZR@256x_' + items[0];
                downloadPatchedZipFile(data, filename, mapName, patchWith256xTech);
            } else {
                downloadPatchedRmsFile(data, '256x_' + filename, mapName, patchWith256xTech);
            }
        }).fail(function () {
            alert("Oops! Could not download rms script.");
        });
    });

    $('.explodingVillagersButton').unbind().click(function (event) {
        let url = $(event.target).closest('.btn-group').find('.map-download').attr('href');
        let mapName = $(event.target).closest('.map-info').find('.card-title a').text();
        let filename = getFilename(url);
        $.ajax({
            url: url,
            beforeSend: function (xhr) {
                xhr.overrideMimeType("text/plain; charset=x-user-defined");
            }
        }).done(function (data) {
            if (data.startsWith('PK\x03\x04')) {
                const items = filename.split('@', 2);
                filename = items.length === 2 ? 'ZR@EV_' + items[1] : 'ZR@EV_' + items[0];
                downloadPatchedZipFile(data, filename, mapName, patchWithExplodingVillagers);
            } else {
                downloadPatchedRmsFile(data, 'EV_' + filename, mapName, patchWithExplodingVillagers);
            }
        }).fail(function () {
            alert("Oops! Could not download rms script.");
        });
    });

    $('.suddenDeathButton').unbind().click(function (event) {
        let url = $(event.target).closest('.btn-group').find('.map-download').attr('href');
        let mapName = $(event.target).closest('.map-info').find('.card-title a').text();
        let filename = getFilename(url);
        $.ajax({
            url: url,
            beforeSend: function (xhr) {
                xhr.overrideMimeType("text/plain; charset=x-user-defined");
            }
        }).done(function (data) {
            if (data.startsWith('PK\x03\x04')) {
                const items = filename.split('@', 2);
                filename = items.length === 2 ? 'ZR@SD_' + items[1] : 'ZR@SD_' + items[0];
                downloadPatchedZipFile(data, filename, mapName, patchWithSuddenDeath);
            } else {
                downloadPatchedRmsFile(data, 'SD_' + filename, mapName, patchWithSuddenDeath);
            }
        }).fail(function () {
            alert("Oops! Could not download rms script.");
        });
    });
}

function getFilename(url) {
    const items = url.split('/');
    return decodeURI(items[items.length - 1]).replace('%40', '@');
}

function patchWith256xTech(content, mapName) {
    content = content.replace(/<PLAYER_SETUP>/g, `/* 256x tech patch part 1 of 2 start */
#const GAAB_101_MIDDLE_AGE 101
#const GAAB_102_FEUDAL_AGE 102
#const GAAB_103_IMPERIAL_AGE 103
#const GAAB_10_TURKISH_ARTILLERY 10
#const GAAB_11_TEUTON_CRENELLATIONS 11
#const GAAB_12_CROP_ROTATION 12
#const GAAB_13_HEAVY_PLOW 13
#const GAAB_140_GUARD_TOWER 140
#const GAAB_14_HORSE_COLLAR 14
#const GAAB_15_GUILDS 15
#const GAAB_16_GOTHIC_ANARCHY 16
#const GAAB_17_BANKING 17
#const GAAB_182_GOLD_SHAFT_MINING 182
#const GAAB_194_FORTIFIED_WALL 194
#const GAAB_199_FLETCHING 199
#const GAAB_19_CARTOGRAPHY 19
#const GAAB_200_BODKIN_ARROW 200
#const GAAB_201_BRACER 201
#const GAAB_202_DOUBLE_BIT_AXE 202
#const GAAB_203_BOW_SAW 203
#const GAAB_211_PADDED_ARCHER_ARMOR 211
#const GAAB_212_LEATHER_ARCHER_ARMOR 212
#const GAAB_213_WHEEL_BARROW 213
#const GAAB_215_SQUIRES 215
#const GAAB_219_RING_ARCHER_ARMOR 219
#const GAAB_21_HUN_ATHEISM 21
#const GAAB_221_TWO_MAN_SAW 221
#const GAAB_22_LOOM 22
#const GAAB_230_BLOCK_PRINTING 230
#const GAAB_231_SANCTITY 231
#const GAAB_233_ILLUMINATION 233
#const GAAB_23_COINAGE 23
#const GAAB_249_HAND_CART 249
#const GAAB_24_AZTEC_GARLAND_WARS 24
#const GAAB_252_FERVOR 252
#const GAAB_278_STONE_MINING 278
#const GAAB_279_STONE_SHAFT_MINING 279
#const GAAB_280_TOWN_PATROL 280
#const GAAB_315_CONSCRIPTION 315
#const GAAB_316_REDEMPTION 316
#const GAAB_319_ATONEMENT 319
#const GAAB_321_SAPPERS 321
#const GAAB_322_MURDER_HOLES 322
#const GAAB_373_SHIPWRIGHT 373
#const GAAB_374_CAREENING 374
#const GAAB_375_DRY_DOCK 375
#const GAAB_377_SIEGE_ENGINEERS 377
#const GAAB_379_HOARDINGS 379
#const GAAB_380_HEATED_SHOT 380
#const GAAB_39_HUSBANDRY 39
#const GAAB_3_BRITISH_YEOMAN 3
#const GAAB_408_SPY_TECHNOLOGY 408
#const GAAB_435_BLOODLINES 435
#const GAAB_436_PARTHIAN_TACTICS 436
#const GAAB_437_THUMB_RING 437
#const GAAB_438_THEOCRACY 438
#const GAAB_439_HERESY 439
#const GAAB_440_SPANISH_SUPREMACY 440
#const GAAB_441_HERBAL_MEDICINE 441
#const GAAB_445_KOREAN_CATAPULTS 445
#const GAAB_457_GOTHIC_PERFUSION 457
#const GAAB_45_FAITH 45
#const GAAB_460_AZTEC_SACRIFICE 460
#const GAAB_461_BRITONS_CITY_RIGHTS 461
#const GAAB_462_CHINESE_GREAT_WALL 462
#const GAAB_463_VIKING_CHIEFTAINS 463
#const GAAB_464_BYZANTINES_GREEK_FIRE 464
#const GAAB_47_CHEMISTRY 47
#const GAAB_482_STRONGHOLD 482
#const GAAB_483_HUNS_UT 483
#const GAAB_484_JAPANESE_UT 484
#const GAAB_485_MAYANS_UT 485
#const GAAB_486_KOREANS_UT 486
#const GAAB_487_MONGOLS_UT 487
#const GAAB_488_PERSIANS_UT 488
#const GAAB_489_TEUTONS_UT 489
#const GAAB_48_CARAVAN 48
#const GAAB_490_SARACENS_UT 490
#const GAAB_491_SIPAHI 491
#const GAAB_492_SPANISH_UT 492
#const GAAB_493_FRANKS_UT 493
#const GAAB_494_PAVISE 494
#const GAAB_499_SILK_ROUTE 499
#const GAAB_49_VIKING_BERSERKERGANG 49
#const GAAB_4_MAYAN_EL_DORADO 4
#const GAAB_506_INDIANS_UT 506
#const GAAB_507_INDIANS_UT2 507
#const GAAB_50_MASONRY 50
#const GAAB_512_SLAVS_UT 512
#const GAAB_513_SLAVS_UT 513
#const GAAB_514_MAGYARS_UT 514
#const GAAB_515_INDIANS_UT 515
#const GAAB_516_INCAS_UT 516
#const GAAB_517_INDIANS_UT 517
#const GAAB_51_ARCHITECTURE 51
#const GAAB_52_CHINESE_ROCKETRY 52
#const GAAB_54_STONE_CUTTING 54
#const GAAB_55_GOLD_MINING 55
#const GAAB_572_PORTUGUESE_UT 572
#const GAAB_573_PORTUGUESE_UT 573
#const GAAB_574_ETHIOPIAN_UT 574
#const GAAB_575_ETHIOPIAN_UT 575
#const GAAB_576_MALIAN_UT 576
#const GAAB_577_MALIAN_UT 577
#const GAAB_578_BERBER_UT 578
#const GAAB_579_BERBER_UT 579
#const GAAB_59_JAPANESE_KATAPARUTO 59
#const GAAB_5_CELTIC_FUROR_CELTICA 5
#const GAAB_602_ARSON 602
#const GAAB_608_ARROWSLITS 608
#const GAAB_61_BYZANTINE_LOGISTICA 61
#const GAAB_622_KHMER_UT 622
#const GAAB_623_KHMER_UT 623
#const GAAB_624_MALAY_UT 624
#const GAAB_625_MALAY_UT 625
#const GAAB_626_BURMESE_UT 626
#const GAAB_627_BURMESE_UT 627
#const GAAB_628_VIETNAMESE_UT 628
#const GAAB_629_VIETNAMESE_UT 629
#const GAAB_63_KEEP 63
#const GAAB_64_BOMBARD_TOWER 64
#const GAAB_65_GILLNETS 65
#const GAAB_67_FORGING 67
#const GAAB_685_KHMER_UT 685
#const GAAB_686_KHMER_UT 686
#const GAAB_687_MALAY_UT 687
#const GAAB_688_MALAY_UT 688
#const GAAB_689_BURMESE_UT 689
#const GAAB_68_IRON_CASTING 68
#const GAAB_690_BURMESE_UT 690
#const GAAB_691_VIETNAMESE_UT 691
#const GAAB_692_VIETNAMESE_UT 692
#const GAAB_6_MONGOL_SIEGE_DRILL 6
#const GAAB_716_TRACKING 716
#const GAAB_74_SCALE_MAIL_ARMOR 74
#const GAAB_754_BURGUNDIAN_VINEYARDS 754
#const GAAB_755_FLEMISH_REVOLUTION 755
#const GAAB_756_FIRST_CRUSADE 756
#const GAAB_757_SCUTAGE 757
#const GAAB_75_BLAST_FURNACE 75
#const GAAB_76_CHAIN_MAIL_ARMOR 76
#const GAAB_77_PLATE_MAIL_ARMOR 77
#const GAAB_7_PERSIAN_MAHOUTS 7
#const GAAB_80_PLATE_BARDING_ARMOR 80
#const GAAB_81_SCALE_BARDING_ARMOR 81
#const GAAB_82_CHAIN_BARDING_ARMOR 82
#const GAAB_83_FRANKISH_BEARDED_AXE 83
#const GAAB_8_TOWN_WATCH 8
#const GAAB_90_TRACKING 90
#const GAAB_93_BALLISTICS 93
#const GAAB_9_SARACEN_ZEALOTRY 9
/* 256x tech patch part 1 of 2 end */
 
<PLAYER_SETUP>
/* 256x tech patch part 2 of 2 start */
effect_amount MODIFY_TECH GAAB_101_MIDDLE_AGE ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_102_FEUDAL_AGE ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_103_IMPERIAL_AGE ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_10_TURKISH_ARTILLERY ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_11_TEUTON_CRENELLATIONS ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_12_CROP_ROTATION ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_13_HEAVY_PLOW ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_140_GUARD_TOWER ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_14_HORSE_COLLAR ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_15_GUILDS ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_16_GOTHIC_ANARCHY ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_17_BANKING ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_182_GOLD_SHAFT_MINING ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_194_FORTIFIED_WALL ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_199_FLETCHING ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_19_CARTOGRAPHY ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_200_BODKIN_ARROW ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_201_BRACER ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_202_DOUBLE_BIT_AXE ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_203_BOW_SAW ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_211_PADDED_ARCHER_ARMOR ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_212_LEATHER_ARCHER_ARMOR ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_213_WHEEL_BARROW ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_215_SQUIRES ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_219_RING_ARCHER_ARMOR ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_21_HUN_ATHEISM ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_221_TWO_MAN_SAW ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_22_LOOM ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_230_BLOCK_PRINTING ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_231_SANCTITY ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_233_ILLUMINATION ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_23_COINAGE ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_249_HAND_CART ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_24_AZTEC_GARLAND_WARS ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_252_FERVOR ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_278_STONE_MINING ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_279_STONE_SHAFT_MINING ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_280_TOWN_PATROL ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_315_CONSCRIPTION ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_316_REDEMPTION ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_319_ATONEMENT ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_321_SAPPERS ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_322_MURDER_HOLES ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_373_SHIPWRIGHT ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_374_CAREENING ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_375_DRY_DOCK ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_377_SIEGE_ENGINEERS ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_379_HOARDINGS ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_380_HEATED_SHOT ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_39_HUSBANDRY ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_3_BRITISH_YEOMAN ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_408_SPY_TECHNOLOGY ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_435_BLOODLINES ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_436_PARTHIAN_TACTICS ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_437_THUMB_RING ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_438_THEOCRACY ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_439_HERESY ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_440_SPANISH_SUPREMACY ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_441_HERBAL_MEDICINE ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_445_KOREAN_CATAPULTS ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_457_GOTHIC_PERFUSION ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_45_FAITH ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_460_AZTEC_SACRIFICE ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_461_BRITONS_CITY_RIGHTS ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_462_CHINESE_GREAT_WALL ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_463_VIKING_CHIEFTAINS ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_464_BYZANTINES_GREEK_FIRE ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_47_CHEMISTRY ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_482_STRONGHOLD ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_483_HUNS_UT ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_484_JAPANESE_UT ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_485_MAYANS_UT ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_486_KOREANS_UT ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_487_MONGOLS_UT ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_488_PERSIANS_UT ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_489_TEUTONS_UT ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_48_CARAVAN ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_490_SARACENS_UT ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_491_SIPAHI ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_492_SPANISH_UT ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_493_FRANKS_UT ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_494_PAVISE ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_499_SILK_ROUTE ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_49_VIKING_BERSERKERGANG ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_4_MAYAN_EL_DORADO ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_506_INDIANS_UT ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_507_INDIANS_UT2 ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_50_MASONRY ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_512_SLAVS_UT ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_513_SLAVS_UT ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_514_MAGYARS_UT ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_515_INDIANS_UT ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_516_INCAS_UT ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_517_INDIANS_UT ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_51_ARCHITECTURE ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_52_CHINESE_ROCKETRY ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_54_STONE_CUTTING ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_55_GOLD_MINING ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_572_PORTUGUESE_UT ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_573_PORTUGUESE_UT ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_574_ETHIOPIAN_UT ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_575_ETHIOPIAN_UT ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_576_MALIAN_UT ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_577_MALIAN_UT ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_578_BERBER_UT ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_579_BERBER_UT ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_59_JAPANESE_KATAPARUTO ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_5_CELTIC_FUROR_CELTICA ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_602_ARSON ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_608_ARROWSLITS ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_61_BYZANTINE_LOGISTICA ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_622_KHMER_UT ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_623_KHMER_UT ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_624_MALAY_UT ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_625_MALAY_UT ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_626_BURMESE_UT ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_627_BURMESE_UT ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_628_VIETNAMESE_UT ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_629_VIETNAMESE_UT ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_63_KEEP ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_64_BOMBARD_TOWER ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_65_GILLNETS ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_67_FORGING ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_685_KHMER_UT ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_686_KHMER_UT ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_687_MALAY_UT ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_688_MALAY_UT ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_689_BURMESE_UT ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_68_IRON_CASTING ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_690_BURMESE_UT ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_691_VIETNAMESE_UT ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_692_VIETNAMESE_UT ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_6_MONGOL_SIEGE_DRILL ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_716_TRACKING ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_74_SCALE_MAIL_ARMOR ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_754_BURGUNDIAN_VINEYARDS ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_755_FLEMISH_REVOLUTION ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_756_FIRST_CRUSADE ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_757_SCUTAGE ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_75_BLAST_FURNACE ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_76_CHAIN_MAIL_ARMOR ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_77_PLATE_MAIL_ARMOR ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_7_PERSIAN_MAHOUTS ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_80_PLATE_BARDING_ARMOR ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_81_SCALE_BARDING_ARMOR ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_82_CHAIN_BARDING_ARMOR ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_83_FRANKISH_BEARDED_AXE ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_8_TOWN_WATCH ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_90_TRACKING ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_93_BALLISTICS ATTR_SET_STACKING 1
effect_amount MODIFY_TECH GAAB_9_SARACEN_ZEALOTRY ATTR_SET_STACKING 1
/* 256x tech patch part 2 of 2 end */\n`);
    content = '/* 256x tech ' + mapName + ' */\n' +
        '/* auto-generated on aoe2map.net */\n\n' + content;
    return content;
}

function patchWithSuddenDeath(content, mapName) {
    if (content.includes('guard_state')) {
        alert('This map already contains a guard_state command.\nSorry, we can\'t patch it automatically.');
        return null;
    }
    content = content.replace(/<PLAYER_SETUP>/g, `/* Sudden Death patch part 1 of 2 start */
#const TOWN_CENTER 109
#const RI_TOWN_CENTER 187 
/* Sudden Death patch part 1 of 2 end */
 
<PLAYER_SETUP>
/* Sudden Death patch part 2 of 2 start */
guard_state TOWN_CENTER AMOUNT_GOLD 0 1
effect_amount ENABLE_TECH RI_TOWN_CENTER ATTR_DISABLE 187
/* Sudden Death patch part 2 of 2 end */\n`);
    content = '/* Sudden Death ' + mapName + ' */\n' +
        '/* auto-generated on aoe2map.net */\n\n' + content;
    return content;
}

function patchWithExplodingVillagers(content, mapName) {
    content = content.replace(/<PLAYER_SETUP>/g, `<PLAYER_SETUP>
/* Exploding villagers patch start */
effect_amount SET_ATTRIBUTE VILLAGER_CLASS ATTR_DEAD_ID 706
effect_amount SET_ATTRIBUTE SABOTEUR ATTR_HITPOINTS 0
effect_amount SET_ATTRIBUTE SABOTEUR ATTR_ATTACK 50
effect_amount SET_ATTRIBUTE SABOTEUR ATTR_ATTACK 346
effect_amount SET_ATTRIBUTE SABOTEUR ATTR_ATTACK 512
effect_amount SET_ATTRIBUTE SABOTEUR ATTR_MAX_RANGE 2
effect_amount SET_ATTRIBUTE SABOTEUR ATTR_BLAST_LEVEL 1
/* Exploding villagers patch end */\n`);
    content = '/* Exploding Villagers ' + mapName + ' */\n' +
        '/* auto-generated on aoe2map.net */\n\n' + content;
    return content;
}

function getMapName(){
    return $('.card-title a').text();
}

function downloadPatchedRmsFile(content, filename, mapName, patch) {
    content = patch(content, mapName);
    if (content === null) {
        return;
    }
    const blob = new Blob([content], {type: "text/plain;charset=utf-8"});
    saveAs(blob, filename);
}

function downloadPatchedZipFile(data, zipFilename, mapName, patch) {
    JSZip.loadAsync(data).then(function (d) {
        for (let filename in d.files) {
            if (d.files.hasOwnProperty(filename)) {
                if (filename.endsWith('.rms')) {
                    let currentRmsFileName = filename;
                    d.file(filename).async('text').then(function (content) {
                        content = patch(content, mapName);
                        if (content === null) {
                            return;
                        }
                        d.file(filename, content);
                        d.generateAsync({type: "blob"}).then(function (blob) {
                            saveAs(blob, zipFilename);
                        });
                    });
                    return;
                }
            }
        }
        alert("No .rms file found inside the archive!");
    });
}