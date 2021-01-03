import enum
import random
import lorem
import argparse

from sqlalchemy import create_engine, Table, Integer, String, Column, Enum
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base



##### supporting models #####

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


##### the main model #####

# psql base class to extend
Base = declarative_base()

""" model the 'State' in the database """
class State(Base):

    # monstrous constructor that simulates the data upon init
    def __init__(self, name):

      # the name is provided in the construction
      self.stateName = name

      # generate a random grade for now
      self.overallGrade = Grade.randomGrade()

      # randomize definition of domestic violence related scores
      self.definitionOfDomesticViolenceGrade = Grade.randomGrade()
      self.workerProtectionsGrade = Grade.randomGrade()
      self.civilRemediesGrade = Grade.randomGrade()
      self.victinsOfCrimeCompensationGrade = Grade.randomGrade()
      self.safteyNetProgramsGrade = Grade.randomGrade()
      self.housingAndRentalProgramsGrade = Grade.randomGrade()
      self.coercedAndFraudulentDebtProtectionsGrade = Grade.randomGrade()
      self.nonCarceralResponseToDomesticViolenceGrade = Grade.randomGrade()
      self.statePublicfuncdingGrade = Grade.randomGrade()

      # randomize economic abuse scores
      self.includesEconomicAbuseFramework = Check.randomCheckScore()
      self.usesCoerciveControlFramework = Check.randomCheckScore()
      self.definitionPolicyRecomendations = Check.randomCheckScore()
      self.protectedSafeLeave = Check.randomCheckScore()
      self.paidSafeLeave = Check.randomCheckScore()
      self.survivorsProtectedAgainstDescrimninationByTheirEmployer = Check.randomCheckScore()
      self.employerMustProvideReasonableWorkAccomodations = Check.randomCheckScore()
      self.protectionAgainstEmployerRelatiationForRequestingAccomodations = Check.randomCheckScore()
      self.employerRequiredToKeepSurvivorStatusConfidential = Check.randomCheckScore()
      self.proofOfSurvivorStatusDoesntRequirePoliceReport = Check.randomCheckScore()
      self.stateHasDesignatedDomesticViolenceTort = Check.randomCheckScore()
      self.statuteOfLimitationsHasXXYearsOrMoreStatue = Check.randomCheckScore()
      self.protectionAgainstLitigationAbuse = Check.randomCheckScore()
      self.survivorsOfDomesticViolenceAreEligibleForFunds = Check.randomCheckScore()
      self.statuteOfLimitationsHasXXYearsOrMore = Check.randomCheckScore()
      self.noCostsForSurvivorToApplyForFunds = Check.randomCheckScore()
      self.offersComprehensiveListOfConvertedInjuriesAndDamages = Check.randomCheckScore()
      self.maximumReimbursmentMoreThanXXDollars = Check.randomCheckScore()
      self.survivorsExemptOrDefferedFromSnapWorkRequirements = Check.randomCheckScore()
      self.survivorsExemptOrDefferedFromTanfWorkRequirements = Check.randomCheckScore()
      self.survivorsEligibleForUnemploymentInsuranceBenefits = Check.randomCheckScore()
      self.nonCitizenSurvivorsAreEligibleForPublicBenefitsOrSocialServices = Check.randomCheckScore()
      self.eleigibleToTerminateRentalLeaseEarly = Check.randomCheckScore()
      self.allowSurvivorToOmitCreditScoreOnRentalApplication = Check.randomCheckScore()
      self.stateOffersForeclosureProtectionsForSurvivors = Check.randomCheckScore()
      self.offersDebtReliefForSurvivors = Check.randomCheckScore()
      self.offersFreeCreditReportFreezes = Check.randomCheckScore()
      self.doesntHaveAMandatoryArrestPolicy = Check.randomCheckScore()
      self.doesntHaveMandatoryReportingRequirements = Check.randomCheckScore()
      self.survivorsDontFacePenaltiesForNotCooperatingWithLawEnforcement = Check.randomCheckScore()
      self.survivorsAreProtectedFromHavingToTestifyAgainstTheirHarmDoer = Check.randomCheckScore()
      self.survivorsAreAbleToDropCriminalChargesAgainstTheirHarmDoer = Check.randomCheckScore()
      self.domesticProgramFundingNotTiedToCriminalJusticeFinesAndFees = Check.randomCheckScore()
      self.xxPercentOrMoreOfStateBudgetSupportsDomesticViolenceProgramsOrServices = Check.randomCheckScore()

      # randomize definition of DV related scores
      self.definitionPolicyRecomendations = self.generateLoremText()
      self.workerProtectionsPolicyRecomendations = self.generateLoremText()
      self.civilRemediesPolicyRecomendations = self.generateLoremText()
      self.victimsOfCrimePolicyRecomendations = self.generateLoremText()
      self.safetyNetProgramsPolicyRecomendations = self.generateLoremText()
      self.housingAndRentalProgramsPolicyRecomendations = self.generateLoremText()
      self.coercedAndFraudulentDebtProtectionsPolicyRecomendations = self.generateLoremText()
      self.nonCarceralResponseToDomesticViolencePolicyRecomendations = self.generateLoremText()
      self.statePublicFundingPolicyRecomendations = self.generateLoremText()
    


    ### properties of the table
    __tablename__ = 'state'
    id = Column(Integer, primary_key = True)
    stateName = Column(String(30), nullable = False)
    overallGrade = Column(Enum(Grade), nullable = False)


    # make a random sentence - this was more complex in a previous version of lorem
    # so I am leaving it here in case we want to pass arguments etc
    def generateLoremText(self):
      return lorem.sentence()



    ### the columns are their types

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

# end of class State



##### simulate and enter into db #####


# collect and unpack command line arguments
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
  default = "1234"
)
parser.add_argument(
  "-o", "--host",
  help = "the host, ie, '@localhost...'",
  default = 'localhost'
)
parser.add_argument(
  "-ot", "--port",
  help = "the port, ie, '...5432/'",
  default = '5432'
)
parser.add_argument(
  "-d", "--database",
  help = "database to connect to, ie, 'freefrom_map_dev'",
  default = "freefrom_map_dev"
)

# get the arguments
args = parser.parse_args()

# assemble the strng for the engine from args
engineString = args.driver + "://" + \
               args.user + ":" + \
               args.password + "@" + \
               args.host + ":" + \
               args.port + "/" + \
               args.database

# create a db connection engine
db = create_engine(engineString)

# create a sesison from the engine
Session = sessionmaker(db)  
session = Session()

# create schema
Base.metadata.create_all(db)



##### generate state data and enter it into the database #####

# dict of states and abbreviations
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


### simulate the dataset and add it to the database

# for each state...
for state in states.values():
  # ... generate a random score for it and add it to the db session
  session.add(State(state))

# push
session.commit()
