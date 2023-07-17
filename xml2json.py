import streamlit as st 
import xml.etree.ElementTree as et
import pandas as pd
import json


st.title('Extract Data from XML')

file = st.file_uploader("Upload XML file here", type=['xml'])

if file is not None:
    st.write("**File uploaded successfully.**")
    # st.write("Parsing XML file...")


    tree=et.parse(file)
    root=tree.getroot()


    tags=[]
    texts=[]
    for i in root.iter():
        
        tags.append(i.tag)
        
        texts.append(i.text) 

    
    df_xml=pd.DataFrame({'tags':tags,'texts':texts}) 

    import re
    def func1(text):

        result = re.sub(r'\{.*?\}', '', text)
        return result
    

    df_xml['tag_extract']=df_xml['tags'].apply(func1)

    df=df_xml[['tag_extract','texts']]

    df.drop_duplicates(inplace=True)
    df.columns=['Element Name','Fact Value']
    # st.write(df)
    def func(element):

        try:
            ans=df[df['Element Name']==element]['Fact Value'].values[0]

            return ans

        except:
            return 'not found'



    name=func('NameOfTheCompany')
    symbol=func('Symbol')
    scrip_code=func('ScripCode')
    start_date=func('DateOfStartOfReportingPeriod')
    end_date=func('DateOfEndOfReportingPeriod')
    report_type=func('NatureOfReportStandaloneConsolidated')


    #non current assets
    property_plant_equipment=func('PropertyPlantAndEquipment')
    capital_work_in_progress=func('CapitalWorkInProgress')
    investment_properties=func('InvestmentProperty')
    good_will=func('Goodwill')
    other_intagible_assets=func('OtherIntangibleAssets')
    right_of_use_assets=func('RightOfUseAssets')
    intangible_assets_under_devlopment=func('IntangibleAssetsUnderDevelopment')
    investment_accounted_using_equity_method=func('InvestmentsAccountedForUsingEquityMethod')
    biological_assets=func('ProceedsFromBiologicalAssetsOtherThanBearerPlantsClassifiedAsInvestingActivities')
    non_current_investments=func('NoncurrentInvestments')
    non_current_loans=func('LoansNoncurrent')
    non_current_financial_assets=func('NoncurrentFinancialAssets')
    non_current_incometax_assets=func('NoncurrentIncomeTaxAssets')
    other_non_current_financial_assets=func('OtherNoncurrentFinancialAssets')
    other_non_current_assets=func('OtherNoncurrentAssets')
    non_current_deferredtax=func('DeferredTax')
    non_current_deferredtax_net=func('DeferredTaxAssetsNet')
    total_non_current_assets=func('NoncurrentAssets')

    #current assets
    current_inventory_assets=func('Inventories')
    current_investments=func('CurrentInvestments')
    current_trade_receivables=func('TradeReceivablesCurrent')
    cash_and_cash_equivalents=func('CashAndCashEquivalents')
    bank_balance_other_than_cash_equivalent=func('BankBalanceOtherThanCashAndCashEquivalents')
    current_loans=func('LoansCurrent')
    other_current_financial_assets=func('OtherCurrentFinancialAssets')
    other_current_assets=func('OtherCurrentAssets')
    other_current_income_tax_assets=func('OthercurrentIncomeTaxAssets')
    other_current_assets_for_sale=func('NoncurrentAssetsClassifiedAsHeldForSale')
    total_assets=func('Assets')

    #equity
    equity_share_capital=func('EquityShareCapital')
    other_equity=func('OtherEquity')
    # non_controlling_interest=func('ComprehensiveIncomeForThePeriodAttributableToOwnersOfParentNonControllingInterests')
    non_controlling_interest=func('NonControllingInterest')
    equity_attributable_to_owners_of_parent=func('EquityAttributableToOwnersOfParent')
    total_equity=func('Equity')


    #non current liabilities
    non_current_borrowing=func('BorrowingsNoncurrent')
    other_non_current_financial_liabilities=func('OtherNoncurrentFinancialLiabilities')
    non_current_lease_liabilities=func('PaymentsOfFinanceLeaseLiabilitiesClassifiedAsFinancingActivities')
    other_non_current_liabilities=func('OtherNoncurrentFinancialLiabilities')
    non_current_deferredtax_liabilities_net=func('DeferredTaxLiabilitiesNet')
    other_non_current_liabilities=func('OtherNoncurrentLiabilities')
    provisions_non_current=func('ProvisionsNoncurrent')
    government_grants=func('ProceedsFromGovernmentGrantsClassifiedAsInvestingActivities')
    total_non_current_liabilities=func('NoncurrentLiabilities')


    #current Liabilities
    current_borrowing=func('BorrowingsCurrent')
    total_assets=func('Assets')
    total_current_assets=func('CurrentAssets')
    dues_of_micro_enterprises=func('DuesOfMicroEnterprises')
    dues_of_creditors=func('DueOfCreditors')
    current_financial_liabilities=func('CurrentFinancialLiabilities')
    # current_lease_liabilities=func('PaymentsOfLeaseLiabilitiesClassifiedAsFinancingActivities')
    current_lease_liabilities=func('CostOfMaterialsConsumed')
    other_current_liabilites=func('OtherCurrentLiabilities')
    other_current_financial_liabilities=func('OtherCurrentFinancialLiabilities')
    current_provisions=func('ProvisionsCurrent')
    current_tax_liabilities=func('CurrentTaxLiabilities')
    # current_government_grant=func('ProceedsFromGovernmentGrantsClassifiedAsInvestingActivities')
    current_government_grant=func('DeferredGovernmentGrantsCurrent')
    total_current_liabilities=func('CurrentLiabilities')
    total_equity_liabilities=func('EquityAndLiabilities')
    trade_payable_current=func('TradePayablesCurrent')



    json_data = {
        "company details":{
            
            "Name":name,
            "Symbol":symbol,
            "scrip Code":scrip_code,
            
            
            
            
            
        },
        
        "Report Details":{
            
            "quarter start date":start_date,
            "quarter end date":end_date,
            'report Type':report_type
            
        },
        "Assets": {
            "Non-current assets": {
                "Property, plant and equipment": property_plant_equipment,
                "Capital work-in-progress": capital_work_in_progress,
                "Investment properties": investment_properties,
                "Goodwill": good_will,
                "Other intangible assets + right of use": other_intagible_assets,
    #             "Right of use assets": right_of_use_assets,
                "Intangible assets under development": intangible_assets_under_devlopment,
                "Investments accounted using equity method": investment_accounted_using_equity_method,
                "Biological assets other than bearer plant": biological_assets,
                "Financial assets": {
                    "Investments": non_current_investments,
                    "Loans": non_current_loans,
                    "Other financial assets": other_non_current_financial_assets
                },
                "Income tax assets": non_current_incometax_assets,
                "Other non-current assets": other_non_current_assets,
                "Deferred tax assets net": non_current_deferredtax_net,
                "Total Non-Current Assets": total_non_current_assets
            },
            "Current Assets": {
                "Inventories": current_inventory_assets,
                "Financial assets": {
                    "Investments": current_investments,
                    "Trade receivables":  current_trade_receivables,
                    "Cash and cash equivalents":cash_and_cash_equivalents,
                    "Bank balances other than": bank_balance_other_than_cash_equivalent,
                    "Loans": current_loans,
                    "Other financial assets": other_current_financial_assets
                },
                "Other current assets": other_current_assets,
                "Income Tax Assets": other_current_income_tax_assets,
                "Total Current Assets": total_current_assets,
                "Assets held for sale": other_current_assets_for_sale,
            },
            "Total Assets": total_assets,
        },
        "Equity and Liabilities": {
            "Equity": {
                "Equity share capital": equity_share_capital,
                "Other equity": other_equity,
                "Non-controlling interest": non_controlling_interest,
                "Equity attributable to Owners of the Parent": equity_attributable_to_owners_of_parent,
                "Total equity": total_equity
            },
            "Non-current liabilities": {
                "Financial liabilities": {
                    "Borrowings": non_current_borrowing,
                    "Other financial liabilities": other_non_current_financial_assets,
                    "non current Lease liabilities": non_current_lease_liabilities
                },
                "Other non-current liabilities": other_non_current_liabilities,
                "Provisions non-current":provisions_non_current,
                "Deferred tax liabilities net": non_current_deferredtax_liabilities_net,
                "Government Grants": government_grants,
                "Total Non-current liabilities": total_non_current_liabilities
            },
            "Current liabilities": {
                "Financial liabilities": {
                    "Borrowings": current_borrowing,
                    "Total outstanding dues of micro enterprises and small enterprises": dues_of_micro_enterprises,
                    "Total outstanding dues of creditors other than micro enterprises and small enterprises": dues_of_creditors,
                    "Trade Payable current (sum of upper two)":trade_payable_current,
                    "Other current financial liabilities": other_current_financial_liabilities,
                    "current Lease liabilities": current_lease_liabilities
                },
                "Other current liabilities": other_current_liabilites,
                "Provisions": current_provisions,
                "Current tax liabilities": current_tax_liabilities,
                "Government Grants": current_government_grant,
                "Total Current liabilities": total_current_liabilities
            },
            "Total Equity and Liabilities":total_equity_liabilities,
        }
    }

    st.subheader('Data from XML')
    st.json(json_data)
    # st.write(json.dumps(json_data,indent=4))