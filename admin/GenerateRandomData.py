import enum
import random
import lorem
import argparse

from sqlalchemy import create_engine, Table, Integer, String, Column, Enum
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# db = create_engine('postgresql+psycopg2://freefrom_map_user:1234"@localhost:5432/freefrom_map_dev')

parser = argparse.ArgumentParser()

parser.add_argument(
  "-r", "--driver",
  help = "Postgres driver for engine creating, ie, 'postgresql+psycopg2://'",
  default = "postgresql+psycopg2"
)
parser.add_argument(
  "-u", "--user",
  help = "Username, ie, 'freefrom_map_user'",
  default = "freefrom_map_user"
)
parser.add_argument(
  "-p", "--password",
  help = "paswword, ie, '1234'",
  default = "'1234'"
)
parser.add_argument(
  "-o", "--host",
  help = "the host, ie, '@localhost...'",
  default = 'localhost'
)
parser.add_argument(
  "-ot", "--port",
  help = "the host, ie, '...54321/'",
  default = '54321'
)
parser.add_argument(
  "-d", "--database",
  help = "database to connect to, ie, 'freefrom_map_dev'",
  default = "freefrom_map_dev"
)

args = parser.parse_args()

# assemble the strng for the engine from args
engineString = args.driver + "://" + \
               args.user + ":" + \
               args.password + "@" + \
               args.host + ":" + \
               args.port + "/" + \
               args.database



""" a 'Grade' type for the states to have """
class Grade(enum.Enum):
    
    # the states a grade can have
    A = 5
    B = 4
    C = 3
    D = 2
    F = 1

    # mapping the states to a string version of themselves to work with str()
    def __str__(self):
      v = self.value
      valueDict = {5:'A', 4:'B', 3:'C', 2:'D', 1:'F'}
      return valueDict[v]

    # get a random grade
    def randomGrade():
      return random.choice([Grade.A, Grade.B, Grade.C, Grade.D, Grade.F])




""" a 'Check' type for rating sub-parts of grade """
class Check(enum.Enum):
    
    # the states a check can have
    CheckPlus = 3
    Check = 2
    CheckMinus = 1


    # mapping the levels to a string version of themselves to work with str()
    def __str__(self):
      v = self.value
      valueDict = {3:'Check+', 2:'Check', 1:'Check-'}
      return valueDict[v]

    # get a random score
    def randomCheckScore():
      return random.choice([Check.CheckPlus, Check.Check, Check.CheckMinus])



Base = declarative_base()
""" model the 'State' in the database """
class State(Base):



    def __init__(self, name):
      self.stateName = name
    


    __tablename__ = 'state'

    id = Column(Integer, primary_key = True)
    stateName = Column(String(30), nullable = False)
    overallGrade = Column(Enum(Grade), nullable = False)


    # definition of domestic violence 
    definitionOfDomesticViolenceGrade = Column(Enum(Grade), nullable = False)
    includesEconomicAbuseFramework = Column(Enum(Check), nullable = False)
    usesCoerciveControlFramework = Column(Enum(Check), nullable = False)

    definitionPolicyRecomendations = Column(String(250), nullable = False)



    # worker protections
    workerProtectionsGrade = Column(Enum(Grade), nullable = False)

    protectedSafeLeave = Column(Enum(Check), nullable = False)
    paidSafeLeave = Column(Enum(Check), nullable = False)
    survivorsProtectedAgainstDescrimninationByTheirEmployer = Column(Enum(Check), nullable = False)
    employerMustProvideReasonableWorkAccomodations = Column(Enum(Check), nullable = False)
    protectionAgainstEmployerRelatiationForRequestingAccomodations = Column(Enum(Check), nullable = False)
    employerRequiredToKeepSurvivorStatusConfidential = Column(Enum(Check), nullable = False)
    proofOfSurvivorStatusDoesntRequirePoliceReport = Column(Enum(Check), nullable = False)

    workerProtectionsPolicyRecomendations = Column(String(250), nullable = False)



    # civil remedies
    civilRemediesGrade = Column(Enum(Grade), nullable = False)

    stateHasDesignatedDomesticViolenceTort = Column(Enum(Check), nullable = False)
    statuteOfLimitationsHasXXYearsOrMoreStatue = Column(Enum(Check), nullable = False)
    protectionAgainstLitigationAbuse = Column(Enum(Check), nullable = False)

    civilRemediesPolicyRecomendations = Column(String(250), nullable = False)



    # victims of crime componsation
    victinsOfCrimeCompensationGrade = Column(Enum(Grade), nullable = False)
    
    survivorsOfDomesticViolenceAreEligibleForFunds = Column(Enum(Check), nullable = False)
    statuteOfLimitationsHasXXYearsOrMore = Column(Enum(Check), nullable = False)
    noCostsForSurvivorToApplyForFunds = Column(Enum(Check), nullable = False)
    offersComprehensiveListOfConvertedInjuriesAndDamages = Column(Enum(Check), nullable = False)
    maximumReimbursmentMoreThanXXDollars = Column(Enum(Check), nullable = False)

    victimsOfCrimePolicyRecomendations = Column(String(250), nullable = False)



    # safety net programs 
    safteyNetProgramsGrade = Column(Enum(Grade), nullable = False)

    survivorsExemptOrDefferedFromSnapWorkRequirements = Column(Enum(Check), nullable = False)
    survivorsExemptOrDefferedFromTanfWorkRequirements = Column(Enum(Check), nullable = False)
    survivorsEligibleForUnemploymentInsuranceBenefits = Column(Enum(Check), nullable = False)
    nonCitizenSurvivorsAreEligibleForPublicBenefitsOrSocialServices = Column(Enum(Check), nullable = False)

    safetyNetProgramsPolicyRecomendations = Column(String(250), nullable = False)




    # housing and rental protections
    housingAndRentalProgramsGrade = Column(Enum(Grade), nullable = False)

    eleigibleToTerminateRentalLeaseEarly =  Column(Enum(Check), nullable = False)
    allowSurvivorToOmitCreditScoreOnRentalApplication = Column(Enum(Check), nullable = False)
    stateOffersForeclosureProtectionsForSurvivors = Column(Enum(Check), nullable = False)

    housingAndRentalProgramsPolicyRecomendations = Column(String(250), nullable = False)



    # coerced and fraudulence debt programs
    coercedAndFraudulentDebtProtectionsGrade = Column(Enum(Grade), nullable = False)

    offersDebtReliefForSurvivors = Column(Enum(Check), nullable = False)
    offersFreeCreditReportFreezes = Column(Enum(Check), nullable = False)

    coercedAndFraudulentDebtProtectionsPolicyRecomendations = Column(String(250), nullable = False)



    # Non-carceral response to domestic violence
    nonCarceralResponseToDomesticViolenceGrade = Column(Enum(Grade), nullable = False)

    doesntHaveAMandatoryArrestPolicy = Column(Enum(Check), nullable = False)
    doesntHaveMandatoryReportingRequirements = Column(Enum(Check), nullable = False)
    survivorsDontFacePenaltiesForNotCooperatingWithLawEnforcement = Column(Enum(Check), nullable = False)
    survivorsAreProtectedFromHavingToTestifyAgainstTheirHarmDoer = Column(Enum(Check), nullable = False)
    survivorsAreAbleToDropCriminalChargesAgainstTheirHarmDoer =  Column(Enum(Check), nullable = False)
    domesticProgramFundingNotTiedToCriminalJusticeFinesAndFees = Column(Enum(Check), nullable = False)

    nonCarceralResponseToDomesticViolencePolicyRecomendations = Column(String(250), nullable = False)



    # state public funding
    statePublicfuncdingGrade = Column(Enum(Grade), nullable = False)

    xxPercentOrMoreOfStateBudgetSupportsDomesticViolenceProgramsOrServices = Column(Enum(Check), nullable = False)

    statePublicFundingPolicyRecomendations = Column(String(250), nullable = False)


states = {
  'AK': 'Alaska',
  'AL': 'Alabama',
  'AR': 'Arkansas',
  'AZ': 'Arizona',
  'CA': 'California',
  'CO': 'Colorado',
  'CT': 'Connecticut',
  'DE': 'Delaware',
  'FL': 'Florida',
  'GA': 'Georgia',
  'HI': 'Hawaii',
  'IA': 'Iowa',
  'ID': 'Idaho',
  'IL': 'Illinois',
  'IN': 'Indiana',
  'KS': 'Kansas',
  'KY': 'Kentucky',
  'LA': 'Louisiana',
  'MA': 'Massachusetts',
  'MD': 'Maryland',
  'ME': 'Maine',
  'MI': 'Michigan',
  'MN': 'Minnesota',
  'MO': 'Missouri',
  'MS': 'Mississippi',
  'MT': 'Montana',
  'NC': 'North Carolina',
  'ND': 'North Dakota',
  'NE': 'Nebraska',
  'NH': 'New Hampshire',
  'NJ': 'New Jersey',
  'NM': 'New Mexico',
  'NV': 'Nevada',
  'NY': 'New York',
  'OH': 'Ohio',
  'OK': 'Oklahoma',
  'OR': 'Oregon',
  'PA': 'Pennsylvania',
  'RI': 'Rhode Island',
  'SC': 'South Carolina',
  'SD': 'South Dakota',
  'TN': 'Tennessee',
  'TX': 'Texas',
  'UT': 'Utah',
  'VA': 'Virginia',
  'VT': 'Vermont',
  'WA': 'Washington',
  'WI': 'Wisconsin',
  'WV': 'West Virginia',
  'WY': 'Wyoming'
}

def generateLoremText():
  return lorem.sentence()

""" simulare the dataset and add it to the database """ 

db = create_engine("postgresql+psycopg2://freefrom_map_user:1234@localhost:5432/freefrom_map_dev")

Session = sessionmaker(db)  
session = Session()
Base.metadata.create_all(db)

jsonDumpList = []

for state in states.values():

  stateObj = State(state)

  stateObj.overallGrade = Grade.randomGrade()
  stateObj.definitionOfDomesticViolenceGrade = Grade.randomGrade()
  stateObj.workerProtectionsGrade = Grade.randomGrade()
  stateObj.civilRemediesGrade = Grade.randomGrade()
  stateObj.victinsOfCrimeCompensationGrade = Grade.randomGrade()
  stateObj.safteyNetProgramsGrade = Grade.randomGrade()
  stateObj.housingAndRentalProgramsGrade = Grade.randomGrade()
  stateObj.coercedAndFraudulentDebtProtectionsGrade = Grade.randomGrade()
  stateObj.nonCarceralResponseToDomesticViolenceGrade = Grade.randomGrade()
  stateObj.statePublicfuncdingGrade = Grade.randomGrade()

  stateObj.includesEconomicAbuseFramework = Check.randomCheckScore()
  stateObj.usesCoerciveControlFramework = Check.randomCheckScore()
  stateObj.definitionPolicyRecomendations = Check.randomCheckScore()
  stateObj.protectedSafeLeave = Check.randomCheckScore()
  stateObj.paidSafeLeave = Check.randomCheckScore()
  stateObj.survivorsProtectedAgainstDescrimninationByTheirEmployer = Check.randomCheckScore()
  stateObj.employerMustProvideReasonableWorkAccomodations = Check.randomCheckScore()
  stateObj.protectionAgainstEmployerRelatiationForRequestingAccomodations = Check.randomCheckScore()
  stateObj.employerRequiredToKeepSurvivorStatusConfidential = Check.randomCheckScore()
  stateObj.proofOfSurvivorStatusDoesntRequirePoliceReport = Check.randomCheckScore()
  stateObj.stateHasDesignatedDomesticViolenceTort = Check.randomCheckScore()
  stateObj.statuteOfLimitationsHasXXYearsOrMoreStatue = Check.randomCheckScore()
  stateObj.protectionAgainstLitigationAbuse = Check.randomCheckScore()
  stateObj.survivorsOfDomesticViolenceAreEligibleForFunds = Check.randomCheckScore()
  stateObj.statuteOfLimitationsHasXXYearsOrMore = Check.randomCheckScore()
  stateObj.noCostsForSurvivorToApplyForFunds = Check.randomCheckScore()
  stateObj.offersComprehensiveListOfConvertedInjuriesAndDamages = Check.randomCheckScore()
  stateObj.maximumReimbursmentMoreThanXXDollars = Check.randomCheckScore()
  stateObj.survivorsExemptOrDefferedFromSnapWorkRequirements = Check.randomCheckScore()
  stateObj.survivorsExemptOrDefferedFromTanfWorkRequirements = Check.randomCheckScore()
  stateObj.survivorsEligibleForUnemploymentInsuranceBenefits = Check.randomCheckScore()
  stateObj.nonCitizenSurvivorsAreEligibleForPublicBenefitsOrSocialServices = Check.randomCheckScore()
  stateObj.eleigibleToTerminateRentalLeaseEarly = Check.randomCheckScore()
  stateObj.allowSurvivorToOmitCreditScoreOnRentalApplication = Check.randomCheckScore()
  stateObj.stateOffersForeclosureProtectionsForSurvivors = Check.randomCheckScore()
  stateObj.offersDebtReliefForSurvivors = Check.randomCheckScore()
  stateObj.offersFreeCreditReportFreezes = Check.randomCheckScore()
  stateObj.doesntHaveAMandatoryArrestPolicy = Check.randomCheckScore()
  stateObj.doesntHaveMandatoryReportingRequirements = Check.randomCheckScore()
  stateObj.survivorsDontFacePenaltiesForNotCooperatingWithLawEnforcement = Check.randomCheckScore()
  stateObj.survivorsAreProtectedFromHavingToTestifyAgainstTheirHarmDoer = Check.randomCheckScore()
  stateObj.survivorsAreAbleToDropCriminalChargesAgainstTheirHarmDoer = Check.randomCheckScore()
  stateObj.domesticProgramFundingNotTiedToCriminalJusticeFinesAndFees = Check.randomCheckScore()
  stateObj.xxPercentOrMoreOfStateBudgetSupportsDomesticViolenceProgramsOrServices = Check.randomCheckScore()

  stateObj.definitionPolicyRecomendations = generateLoremText()
  stateObj.workerProtectionsPolicyRecomendations = generateLoremText()
  stateObj.civilRemediesPolicyRecomendations = generateLoremText()
  stateObj.victimsOfCrimePolicyRecomendations = generateLoremText()
  stateObj.safetyNetProgramsPolicyRecomendations = generateLoremText()
  stateObj.housingAndRentalProgramsPolicyRecomendations = generateLoremText()
  stateObj.coercedAndFraudulentDebtProtectionsPolicyRecomendations = generateLoremText()
  stateObj.nonCarceralResponseToDomesticViolencePolicyRecomendations = generateLoremText()
  stateObj.statePublicFundingPolicyRecomendations = generateLoremText()

  session.add(stateObj)



session.commit()
