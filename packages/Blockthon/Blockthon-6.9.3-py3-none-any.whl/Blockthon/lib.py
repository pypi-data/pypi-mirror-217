import hashlib, codecs, binascii, pbkdf2, hmac
import os, base58, random, ecdsa, re, base64
from hashlib import sha256, new, sha512
from typing import Type
from bip32utils import BIP32Key
from mnemonic import Mnemonic

BASE58_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
GROUP_ORDER = (
    b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
    b'\xfe\xba\xae\xdc\xe6\xafH\xa0;\xbf\xd2^\x8c\xd06AA'
)
GROUP_ORDER_INT = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
KEY_SIZE = 32
ZERO = b'\x00'


def sh256k1(data_str: str) -> bytes:
    return sha256(data_str).digest()


def sh256k2(data_str: str) -> bytes:
    return sha256(sha256(data_str).digest()).digest()


def Base58Decode(v):
    if not isinstance(v, str):
        v = v.decode('ascii')
    dec = 0
    for char in v:
        dec = dec * 58 + BASE58_ALPHABET.index(char)
    return dec.to_bytes((dec.bit_length() + 7) // 8, 'big')


def Base58Encode(v):
    p, a = 1, 0
    for c in reversed(v):
        a += p * c
        p = p << 8
    string = ""
    while a:
        a, idx = divmod(a, 58)
        string = BASE58_ALPHABET[idx] + string
    for c in v:
        if c == 0:
            string = BASE58_ALPHABET[0] + string
        else:
            break
    return string


def Base58Encode_Check(ver, payer):
    data = ver + payer
    check = sh256k2(data)[:4]
    return Base58Encode(data + check)


def Base58Decode_Check(v):
    bytes_data = Base58Decode(v)
    Checksum_Actual = sh256k2(bytes_data[:-4])
    Checksum_Expect = bytes_data[-4:]
    if Checksum_Actual[:4] != Checksum_Expect:
        raise ValueError("Invalid Checksum")
    else:
        return bytes_data[:-4]


# Bytes To Hex
def Hexlify(data_str: bytes) -> str:
    """
    convert `bytes` to `hex`
    \n``[ bytes -> hex ]``

    :param data_str:
    :type: bytes.
    :return: string_Hex.
    :type: str.
    """
    return binascii.hexlify(data_str).decode()


# Converting Hex To Bytes
def unHexlify(data_str: str) -> bytes:
    """
    received hex string and convert hex string to bytes
    \n[ hex ---> bytes ]

    :param data_str:
    :type: str.
    :return: bytes_data.
    :type: str.
    """
    return binascii.unhexlify(data_str)


def SH256(bytes_data: bytes) -> any:
    return hashlib.sha256(bytes_data)


def encrypt(data: str) -> str:
    """
    received hex string and encodec with sha256 to hex again (recompile).
    \nhex -> hex

    :param data:
    :type: str.
    :return: hexString.
    :type: str.
    """
    return SH256(unHexlify(data)).hexdigest()


def B58enUnHex(hex_string: str) -> str:
    return base58.b58encode(unHexlify(hex_string)).decode('utf-8')


def getSec() -> str:
    char = 'abcdef1234567890'
    string = ''
    for _ in range(len(char)):
        adder = random.choice(char)
        if adder not in string:
            string += adder
    return string


def from_int(integer: int) -> str:
    """
    convert number or decimal to hex

    :param integer:
    :type: int.
    :return: hexString.
    :type: str.
    """
    return '{:02x}'.format(integer)


def PVK() -> str:
    """
    generated random private key `hex` without repeat.
    received string data from hexadecimal character word `abcdef1234567890`\n
    on in string without repeat. loop process to complete 64 character\n
    and return string hex

    :return: hexString.
    """
    key = ''
    for _ in range(6):
        norepeat = getSec()
        if norepeat not in key:
            key += norepeat
    if len(key) < 64:
        equal = (64 - len(key)) * '0'
        return equal + key
    else:
        return key[0:64]


def DecToHex(dec: int) -> str:
    """
    convert number to hex string
    :param dec:
    :type: int.
    :return: stringHex.
    :type: str.
    """
    decKey = from_int(dec)
    if len(decKey) < 64:
        return decKey.zfill(64)
    else:
        return decKey


def b58_encodec(data: str) -> str:
    """
    convertor hex string to string b58 decode decompile

    :param data:
    :type: str.
    :return: string_b58.
    :type: str.
    """
    return base58.b58encode(unHexlify(data)).decode('utf-8')


def HexToBin(hexed: str) -> str:
    return bin(int(hexed, 16))[2:].zfill(256)


def HexToMne(hex_string: str, size: int = 12) -> str:
    byte_string = unHexlify(hex_string)
    ValidLen = [12, 18, 24]
    if size in ValidLen:
        NearestLen = min(ValidLen, key=lambda x: abs(x - len(byte_string)))
        if len(byte_string) != NearestLen:
            byte_string = byte_string[:NearestLen]
        return Mnemonic('english').to_mnemonic(byte_string)
    else:
        return f"To create a mnemonic, you need to enter the size (number) of words"


def BytsToRIPEMD160(byte: bytes) -> bytes:
    RIPEMD160 = hashlib.new('ripemd160')
    RIPEMD160.update(byte)
    return RIPEMD160.digest()

def BytesToMne(bytes_string: bytes) -> str:
    return Mnemonic('english').to_mnemonic(bytes_string)


def BytesToMnemonic(bytes_string: bytes, size: int) -> str:
    mne = BytesToMne(bytes_string)
    if size == 12:
        return ' '.join(str(mne).split(' ')[0:12])
    elif size == 16:
        return ' '.join(str(mne).split(' ')[0:16])
    elif size == 18:
        return ' '.join(str(mne).split(' ')[0:18])
    elif size == 24:
        return ' '.join(str(mne).split(' ')[0:24])
    else:
        return ' '.join(str(mne).split(' ')[0:12])


def BytesToHex(bytes_string: bytes) -> str:
    return Hexlify(bytes_string)


def BytesToWif(bytes_key: bytes, compress=False) -> str:
    vb = b'\x80'
    cv = b'\x01'
    uv = b''
    if compress:
        bytes_key += cv
    else:
        bytes_key += uv

    return Base58Encode_Check(vb, bytes_key)


def BytesToDec(bytestr: bytes) -> int:
    return int.from_bytes(bytestr, 'big')


def BytesToAddr(bytes_data: bytes, compress=False) -> str:
    from bit import Key
    from bit.format import bytes_to_wif as btw
    if compress:
        wif = btw(bytes_data, compressed=True)
        bits = Key(wif)
        return bits.address
    else:
        wif = btw(bytes_data, compressed=False)
        bits = Key(wif)
        return bits.address


def BytesToPub(bytes_data: bytes, compress=False) -> str:
    from bit import Key
    from bit.format import bytes_to_wif as btw
    if compress:
        wif = btw(bytes_data, compressed=True)
        bits = Key(wif)
        pubbytes = bits.public_key
        return Hexlify(pubbytes)
    else:
        wif = btw(bytes_data, compressed=False)
        bits = Key(wif)
        pubbytes = bits.public_key
        return Hexlify(pubbytes)


def WifAddr(wif: str) -> str:
    from bit import Key
    bits = Key(wif)
    return bits.address


def WifToBytes(wif: str) -> bytes:
    wif_Bytes = Base58Decode_Check(wif)
    return wif_Bytes[1:]


def getMnemonic(size: int) -> str | None:
    ml = ''
    words = "AbandonAbilityAbleAboutAboveAbsentAbsorbAbstractAbsurdAbuseAccessAccidentAccountAccuseAchieveAcidAcousticAcquireAcrossActActionActorActressActualAdaptAddAddictAddressAdjustAdmitAdultAdvanceAdviceAerobicAffairAffordAfraidAgainAgeAgentAgreeAheadAimAirAirportAisleAlarmAlbumAlcoholAlertAlienAllAlleyAllowAlmostAloneAlphaAlreadyAlsoAlterAlwaysAmateurAmazingAmongAmountAmusedAnalystAnchorAncientAngerAngleAngryAnimalAnkleAnnounceAnnualAnotherAnswerAntennaAntiqueAnxietyAnyApartApologyAppearAppleApproveAprilArchArcticAreaArenaArgueArmArmedArmorArmyAroundArrangeArrestArriveArrowArtArtefactArtistArtworkAskAspectAssaultAssetAssistAssumeAsthmaAthleteAtomAttackAttendAttitudeAttractAuctionAuditAugustAuntAuthorAutoAutumnAverageAvocadoAvoidAwakeAwareAwayAwesomeAwfulAwkwardAxisBabyBachelorBaconBadgeBagBalanceBalconyBallBambooBananaBannerBarBarelyBargainBarrelBaseBasicBasketBattleBeachBeanBeautyBecauseBecomeBeefBeforeBeginBehaveBehindBelieveBelowBeltBenchBenefitBestBetrayBetterBetweenBeyondBicycleBidBikeBindBiologyBirdBirthBitterBlackBladeBlameBlanketBlastBleakBlessBlindBloodBlossomBlouseBlueBlurBlushBoardBoatBodyBoilBombBoneBonusBookBoostBorderBoringBorrowBossBottomBounceBoxBoyBracketBrainBrandBrassBraveBreadBreezeBrickBridgeBriefBrightBringBriskBroccoliBrokenBronzeBroomBrotherBrownBrushBubbleBuddyBudgetBuffaloBuildBulbBulkBulletBundleBunkerBurdenBurgerBurstBusBusinessBusyButterBuyerBuzzCabbageCabinCableCactusCageCakeCallCalmCameraCampCanCanalCancelCandyCannonCanoeCanvasCanyonCapableCapitalCaptainCarCarbonCardCargoCarpetCarryCartCaseCashCasinoCastleCasualCatCatalogCatchCategoryCattleCaughtCauseCautionCaveCeilingCeleryCementCensusCenturyCerealCertainChairChalkChampionChangeChaosChapterChargeChaseChatCheapCheckCheeseChefCherryChestChickenChiefChildChimneyChoiceChooseChronicChuckleChunkChurnCigarCinnamonCircleCitizenCityCivilClaimClapClarifyClawClayCleanClerkCleverClickClientCliffClimbClinicClipClockClogCloseClothCloudClownClubClumpClusterClutchCoachCoastCoconutCodeCoffeeCoilCoinCollectColorColumnCombineComeComfortComicCommonCompanyConcertConductConfirmCongressConnectConsiderControlConvinceCookCoolCopperCopyCoralCoreCornCorrectCostCottonCouchCountryCoupleCourseCousinCoverCoyoteCrackCradleCraftCramCraneCrashCraterCrawlCrazyCreamCreditCreekCrewCricketCrimeCrispCriticCropCrossCrouchCrowdCrucialCruelCruiseCrumbleCrunchCrushCryCrystalCubeCultureCupCupboardCuriousCurrentCurtainCurveCushionCustomCuteCycleDadDamageDampDanceDangerDaringDashDaughterDawnDayDealDebateDebrisDecadeDecemberDecideDeclineDecorateDecreaseDeerDefenseDefineDefyDegreeDelayDeliverDemandDemiseDenialDentistDenyDepartDependDepositDepthDeputyDeriveDescribeDesertDesignDeskDespairDestroyDetailDetectDevelopDeviceDevoteDiagramDialDiamondDiaryDiceDieselDietDifferDigitalDignityDilemmaDinnerDinosaurDirectDirtDisagreeDiscoverDiseaseDishDismissDisorderDisplayDistanceDivertDivideDivorceDizzyDoctorDocumentDogDollDolphinDomainDonateDonkeyDonorDoorDoseDoubleDoveDraftDragonDramaDrasticDrawDreamDressDriftDrillDrinkDripDriveDropDrumDryDuckDumbDuneDuringDustDutchDutyDwarfDynamicEagerEagleEarlyEarnEarthEasilyEastEasyEchoEcologyEconomyEdgeEditEducateEffortEggEightEitherElbowElderElectricElegantElementElephantElevatorEliteElseEmbarkEmbodyEmbraceEmergeEmotionEmployEmpowerEmptyEnableEnactEndEndlessEndorseEnemyEnergyEnforceEngageEngineEnhanceEnjoyEnlistEnoughEnrichEnrollEnsureEnterEntireEntryEnvelopeEpisodeEqualEquipEraEraseErodeErosionErrorEruptEscapeEssayEssenceEstateEternalEthicsEvidenceEvilEvokeEvolveExactExampleExcessExchangeExciteExcludeExcuseExecuteExerciseExhaustExhibitExileExistExitExoticExpandExpectExpireExplainExposeExpressExtendExtraEyeEyebrowFabricFaceFacultyFadeFaintFaithFallFalseFameFamilyFamousFanFancyFantasyFarmFashionFatFatalFatherFatigueFaultFavoriteFeatureFebruaryFederalFeeFeedFeelFemaleFenceFestivalFetchFeverFewFiberFictionFieldFigureFileFilmFilterFinalFindFineFingerFinishFireFirmFirstFiscalFishFitFitnessFixFlagFlameFlashFlatFlavorFleeFlightFlipFloatFlockFloorFlowerFluidFlushFlyFoamFocusFogFoilFoldFollowFoodFootForceForestForgetForkFortuneForumForwardFossilFosterFoundFoxFragileFrameFrequentFreshFriendFringeFrogFrontFrostFrownFrozenFruitFuelFunFunnyFurnaceFuryFutureGadgetGainGalaxyGalleryGameGapGarageGarbageGardenGarlicGarmentGasGaspGateGatherGaugeGazeGeneralGeniusGenreGentleGenuineGestureGhostGiantGiftGiggleGingerGiraffeGirlGiveGladGlanceGlareGlassGlideGlimpseGlobeGloomGloryGloveGlowGlueGoatGoddessGoldGoodGooseGorillaGospelGossipGovernGownGrabGraceGrainGrantGrapeGrassGravityGreatGreenGridGriefGritGroceryGroupGrowGruntGuardGuessGuideGuiltGuitarGunGymHabitHairHalfHammerHamsterHandHappyHarborHardHarshHarvestHatHaveHawkHazardHeadHealthHeartHeavyHedgehogHeightHelloHelmetHelpHenHeroHiddenHighHillHintHipHireHistoryHobbyHockeyHoldHoleHolidayHollowHomeHoneyHoodHopeHornHorrorHorseHospitalHostHotelHourHoverHubHugeHumanHumbleHumorHundredHungryHuntHurdleHurryHurtHusbandHybridIceIconIdeaIdentifyIdleIgnoreIllIllegalIllnessImageImitateImmenseImmuneImpactImposeImproveImpulseInchIncludeIncomeIncreaseIndexIndicateIndoorIndustryInfantInflictInformInhaleInheritInitialInjectInjuryInmateInnerInnocentInputInquiryInsaneInsectInsideInspireInstallIntactInterestIntoInvestInviteInvolveIronIslandIsolateIssueItemIvoryJacketJaguarJarJazzJealousJeansJellyJewelJobJoinJokeJourneyJoyJudgeJuiceJumpJungleJuniorJunkJustKangarooKeenKeepKetchupKeyKickKidKidneyKindKingdomKissKitKitchenKiteKittenKiwiKneeKnifeKnockKnowLabLabelLaborLadderLadyLakeLampLanguageLaptopLargeLaterLatinLaughLaundryLavaLawLawnLawsuitLayerLazyLeaderLeafLearnLeaveLectureLeftLegLegalLegendLeisureLemonLendLengthLensLeopardLessonLetterLevelLiarLibertyLibraryLicenseLifeLiftLightLikeLimbLimitLinkLionLiquidListLittleLiveLizardLoadLoanLobsterLocalLockLogicLonelyLongLoopLotteryLoudLoungeLoveLoyalLuckyLuggageLumberLunarLunchLuxuryLyricsMachineMadMagicMagnetMaidMailMainMajorMakeMammalManManageMandateMangoMansionManualMapleMarbleMarchMarginMarineMarketMarriageMaskMassMasterMatchMaterialMathMatrixMatterMaximumMazeMeadowMeanMeasureMeatMechanicMedalMediaMelodyMeltMemberMemoryMentionMenuMercyMergeMeritMerryMeshMessageMetalMethodMiddleMidnightMilkMillionMimicMindMinimumMinorMinuteMiracleMirrorMiseryMissMistakeMixMixedMixtureMobileModelModifyMomMomentMonitorMonkeyMonsterMonthMoonMoralMoreMorningMosquitoMotherMotionMotorMountainMouseMoveMovieMuchMuffinMuleMultiplyMuscleMuseumMushroomMusicMustMutualMyselfMysteryMythNaiveNameNapkinNarrowNastyNationNatureNearNeckNeedNegativeNeglectNeitherNephewNerveNestNetNetworkNeutralNeverNewsNextNiceNightNobleNoiseNomineeNoodleNormalNorthNoseNotableNoteNothingNoticeNovelNowNuclearNumberNurseNutOakObeyObjectObligeObscureObserveObtainObviousOccurOceanOctoberOdorOffOfferOfficeOftenOilOkayOldOliveOlympicOmitOnceOneOnionOnlineOnlyOpenOperaOpinionOpposeOptionOrangeOrbitOrchardOrderOrdinaryOrganOrientOriginalOrphanOstrichOtherOutdoorOuterOutputOutsideOvalOvenOverOwnOwnerOxygenOysterOzonePactPaddlePagePairPalacePalmPandaPanelPanicPantherPaperParadeParentParkParrotPartyPassPatchPathPatientPatrolPatternPausePavePaymentPeacePeanutPearPeasantPelicanPenPenaltyPencilPeoplePepperPerfectPermitPersonPetPhonePhotoPhrasePhysicalPianoPicnicPicturePiecePigPigeonPillPilotPinkPioneerPipePistolPitchPizzaPlacePlanetPlasticPlatePlayPleasePledgePluckPlugPlungePoemPoetPointPolarPolePolicePondPonyPoolPopularPortionPositionPossiblePostPotatoPotteryPovertyPowderPowerPracticePraisePredictPreferPreparePresentPrettyPreventPricePridePrimaryPrintPriorityPrisonPrivatePrizeProblemProcessProduceProfitProgramProjectPromoteProofPropertyProsperProtectProudProvidePublicPuddingPullPulpPulsePumpkinPunchPupilPuppyPurchasePurityPurposePursePushPutPuzzlePyramidQualityQuantumQuarterQuestionQuickQuitQuizQuoteRabbitRaccoonRaceRackRadarRadioRailRainRaiseRallyRampRanchRandomRangeRapidRareRateRatherRavenRawRazorReadyRealReasonRebelRebuildRecallReceiveRecipeRecordRecycleReduceReflectReformRefuseRegionRegretRegularRejectRelaxReleaseReliefRelyRemainRememberRemindRemoveRenderRenewRentReopenRepairRepeatReplaceReportRequireRescueResembleResistResourceResponseResultRetireRetreatReturnReunionRevealReviewRewardRhythmRibRibbonRiceRichRideRidgeRifleRightRigidRingRiotRippleRiskRitualRivalRiverRoadRoastRobotRobustRocketRomanceRoofRookieRoomRoseRotateRoughRoundRouteRoyalRubberRudeRugRuleRunRunwayRuralSadSaddleSadnessSafeSailSaladSalmonSalonSaltSaluteSameSampleSandSatisfySatoshiSauceSausageSaveSayScaleScanScareScatterSceneSchemeSchoolScienceScissorsScorpionScoutScrapScreenScriptScrubSeaSearchSeasonSeatSecondSecretSectionSecuritySeedSeekSegmentSelectSellSeminarSeniorSenseSentenceSeriesServiceSessionSettleSetupSevenShadowShaftShallowShareShedShellSheriffShieldShiftShineShipShiverShockShoeShootShopShortShoulderShoveShrimpShrugShuffleShySiblingSickSideSiegeSightSignSilentSilkSillySilverSimilarSimpleSinceSingSirenSisterSituateSixSizeSkateSketchSkiSkillSkinSkirtSkullSlabSlamSleepSlenderSliceSlideSlightSlimSloganSlotSlowSlushSmallSmartSmileSmokeSmoothSnackSnakeSnapSniffSnowSoapSoccerSocialSockSodaSoftSolarSoldierSolidSolutionSolveSomeoneSongSoonSorrySortSoulSoundSoupSourceSouthSpaceSpareSpatialSpawnSpeakSpecialSpeedSpellSpendSphereSpiceSpiderSpikeSpinSpiritSplitSpoilSponsorSpoonSportSpotSpraySpreadSpringSpySquareSqueezeSquirrelStableStadiumStaffStageStairsStampStandStartStateStaySteakSteelStemStepStereoStickStillStingStockStomachStoneStoolStoryStoveStrategyStreetStrikeStrongStruggleStudentStuffStumbleStyleSubjectSubmitSubwaySuccessSuchSuddenSufferSugarSuggestSuitSummerSunSunnySunsetSuperSupplySupremeSureSurfaceSurgeSurpriseSurroundSurveySuspectSustainSwallowSwampSwapSwarmSwearSweetSwiftSwimSwingSwitchSwordSymbolSymptomSyrupSystemTableTackleTagTailTalentTalkTankTapeTargetTaskTasteTattooTaxiTeachTeamTellTenTenantTennisTentTermTestTextThankThatThemeThenTheoryThereTheyThingThisThoughtThreeThriveThrowThumbThunderTicketTideTigerTiltTimberTimeTinyTipTiredTissueTitleToastTobaccoTodayToddlerToeTogetherToiletTokenTomatoTomorrowToneTongueTonightToolToothTopTopicToppleTorchTornadoTortoiseTossTotalTouristTowardTowerTownToyTrackTradeTrafficTragicTrainTransferTrapTrashTravelTrayTreatTreeTrendTrialTribeTrickTriggerTrimTripTrophyTroubleTruckTrueTrulyTrumpetTrustTruthTryTubeTuitionTumbleTunaTunnelTurkeyTurnTurtleTwelveTwentyTwiceTwinTwistTwoTypeTypicalUglyUmbrellaUnableUnawareUncleUncoverUnderUndoUnfairUnfoldUnhappyUniformUniqueUnitUniverseUnknownUnlockUntilUnusualUnveilUpdateUpgradeUpholdUponUpperUpsetUrbanUrgeUsageUseUsedUsefulUselessUsualUtilityVacantVacuumVagueValidValleyValveVanVanishVaporVariousVastVaultVehicleVelvetVendorVentureVenueVerbVerifyVersionVeryVesselVeteranViableVibrantViciousVictoryVideoViewVillageVintageViolinVirtualVirusVisaVisitVisualVitalVividVocalVoiceVoidVolcanoVolumeVoteVoyageWageWagonWaitWalkWallWalnutWantWarfareWarmWarriorWashWaspWasteWaterWaveWayWealthWeaponWearWeaselWeatherWebWeddingWeekendWeirdWelcomeWestWetWhaleWhatWheatWheelWhenWhereWhipWhisperWideWidthWifeWildWillWinWindowWineWingWinkWinnerWinterWireWisdomWiseWishWitnessWolfWomanWonderWoodWoolWordWorkWorldWorryWorthWrapWreckWrestleWristWriteWrongYardYearYellowYouYoungYouthZebraZeroZoneZoo"
    mnemonics = re.findall('[A-Z][a-z]+', words)
    if size == 12:
        for r in range(size):
            lx = random.choice(mnemonics)
            ml += f" {lx}"
        return str(ml).lower()
    elif size == 18:
        for r in range(size):
            lx = random.choice(mnemonics)
            ml += f" {lx}"
        return str(ml).lower()
    else:
        return None


def MnemToRoot(mnem: str) -> str:
    mnemonic_ = ''.join(c for c in mnem if c.isalnum())
    mnemonic_ = mnemonic_.split(' ')
    seed_ = pbkdf2.PBKDF2(' '.join(mnemonic_), 'mnemonic' + '', iterations=2048, macmodule=hmac,
                          digestmodule=sha512).read(64)
    xprv_ = BIP32Key.fromEntropy(seed_)
    return xprv_.ExtendedKey()


def WordToBytes(mnem: str) -> bytes:
    return Mnemonic("english").to_seed(mnem)


def MnemonicToBytes(mnemonic_words: str) -> bytes:
    seed = BIP32Key.fromEntropy(WordToBytes(mnemonic_words))
    seed_bytes = seed.ChainCode()
    return ValidSecret(seed_bytes)


def PadScalar(scalar: bytes) -> bytes:
    return (ZERO * (KEY_SIZE - len(scalar))) + scalar


def DecToBytes(num: int) -> bytes:
    len_num = num.bit_length()
    return num.to_bytes((len_num + 7) // 8 or 1, 'big')


def DecBytePad(num: int) -> bytes:
    return PadScalar(num.to_bytes((num.bit_length() + 7) // 8 or 1, 'big'))


def ValidSecret(secret: bytes) -> bytes:
    if not 0 < BytesToDec(secret) < GROUP_ORDER_INT:
        raise ValueError(f'Secret scalar must be greater than 0 and less than {GROUP_ORDER_INT}.')
    return PadScalar(secret)


def getBytes(size: int = 32) -> bytes: return os.urandom(size)


def BinToHex(binString: str) -> str:
    return hex(int(binString, 2))[2:].zfill(32)


def getBin(size: int = 256) -> str:
    bin_str = ""
    for _ in range(size):
        bin_str += random.choice(['0', '1'])
    return bin_str


def AddrToH160(addr: str) -> str:
    decodeAddr = base58.b58decode(addr)
    hexAddr = Hexlify(decodeAddr)
    return hexAddr[2:-8]
