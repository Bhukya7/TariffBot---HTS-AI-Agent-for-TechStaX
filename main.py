# main.py
from rag_tool import initialize_rag_chain, answer_query
from tariff_calculator import calculate_duties
import re

class TariffBot:
    def __init__(self):
        self.rag_chain = initialize_rag_chain()
        self.chat_history = []

    def format_tariff_response(self, result):
        if "error" in result:
            return result["error"]
        response = (
            f"HTS Code: {result['HTS_Code']}\n"
            f"CIF Value: ${result['CIF_Value']:.2f}\n"
            f"Duty Rate: {result['Duty_Rate']*100:.2f}%\n"
            f"Duty Amount: ${result['Duty_Amount']:.2f}"
        )
        if "Total_Weight" in result:
            response += f"\nTotal Weight: {result['Total_Weight']} kg"
        return response

    def handle_query(self, query, hts_code=None, product_cost=None, freight=None, insurance=None, unit_weight=None, quantity=None):
        from database import query_by_description
        if "hts code for" in query.lower():
            description = query.lower().split("hts code for")[-1].strip()
            df = query_by_description(description)
            if not df.empty:
                return f"HTS Code for {description}: {df['HTS_Number'].iloc[0]}\nDescription: {df['Description'].iloc[0]}"
            return f"No HTS code found for {description}"
        if hts_code:
            result = calculate_duties(hts_code, product_cost, freight, insurance, unit_weight, quantity)
            return self.format_tariff_response(result)
        else:
            answer, sources = answer_query(self.rag_chain, query, self.chat_history)
            self.chat_history.append((query, answer))
            return f"{answer}\nSources: {[doc.metadata.get('source', 'N/A') for doc in sources]}"

    def run(self):
        print("Welcome to TariffBot! Type 'exit' to quit.")
        while True:
            query = input("Enter your query: ")
            if query.lower() == 'exit':
                break
            if query.startswith("HTS code"):
                parts = query.split(',')
                hts_code = parts[0].split()[-1].strip()
                product_cost = float(parts[1].split('$')[-1].strip())
                unit_weight = float(re.search(r'[\d.]+', parts[2]).group()) if len(parts) > 2 else None
                quantity = float(re.search(r'[\d.]+', parts[3]).group()) if len(parts) > 3 else None
                response = self.handle_query(query, hts_code, product_cost, unit_weight=unit_weight, quantity=quantity)
            else:
                response = self.handle_query(query)
            print(response)

if __name__ == "__main__":
    bot = TariffBot()
    bot.run()