import pdfplumber
import pandas as pd
from tabulate import tabulate 
import os 
import camelot
import flet as ft
import traceback
import re


def create_output_directory(file_name: str) -> str:
    os.makedirs('output', exist_ok=True)
    first_path = f'output/{file_name}'
    os.makedirs(first_path, exist_ok=True)
    return first_path

def extract_tables_from_pdf(file_name,file_path,youlocation_file):

    # try:
    #     os.mkdir('output') 
    # except FileExistsError:
    #     pass

    # first_path = f'output/{file_name}'
    # try:
    #     os.mkdir(first_path) 
    # except FileExistsError:
    #     pass
    first_path= create_output_directory(file_name)
    pdf = pdfplumber.open(file_path)
    dfs =[]
    for k in range (len(pdf.pages)):
        print(f' page {k+1} of {len(pdf.pages)}')
        print("=--="*5)
        tables = camelot.read_pdf(file_path, pages=str(k+1),flavor='stream')
        column_names = ['Ref','Description', 'Ordered', 'Supplied', 'Unit Price', 'Amount']
        strings_to_drop = ['Chocolate, Sweets & Snacks','Drinks - Hot & Cold','Frozen Foods','Liquor - Wine','Bakery','Baking & Cooking','','Price $','Price','Product ID','Spices & Seasonings','Jams, Honey & Spreads','Condiments & Dressings','Canned & Prepared Foods','Baking Supplies & Sugar','Biscuits & Crackers','Cheese','Confectionery','Desserts','Laundry','Sauces, Stock & Marinades','Snack Foods','Wine',"Here's what was Out of Stock and not supplied","Here's what was substituted and / or modified ","Unit ","Continued from previous page",'Cold Drinks',"Here's what was",'Quant']
        
        for table in tables:
            try:
                df = table.df
                old_df = table.df
                
                for idx, row in df.iterrows():
                        if idx > 1:
                            if all((cell == '' or pd.isnull(cell)) for col, cell in row.items() if col != df.columns[1]):
                                if df.at[idx,df.columns[1]] not in strings_to_drop:
                                    df.at[idx-1,df.columns[1]]=str(df.at[idx-1,df.columns[1]])+' '+str(df.at[idx,df.columns[1]])
                
                
                df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
                
                # Remove rows with empty cells or empty strings in the first column
                df = df[~df[df.columns[0]].isin(['', ' '])]
                
                # Remove rows where the first column is not a number
                df = df[df[df.columns[0]].notna() | df[df.columns[0]].shift().notna()]
                df = df[pd.to_numeric(df[df.columns[0]], errors='coerce').notna()]
                
                # Remove columns that are empty or full of spaces/empty strings
                df = df.dropna(axis=1, how='all')
                df = df.drop(columns=[col for col in df.columns if df[col].isin(['', ' ']).all()])
                
                # Merge rows with only the second cell non-empty
                
                
                # Remove rows with only one non-empty cell
                df[df.columns[0]] = df[df.columns[0]].fillna(method='ffill')
                df[df.columns[1]] = df[df.columns[1]].fillna(method='ffill')
                
                # Remove rows with only one non-empty cell
                # df = df[~df.apply(lambda row: row.count() == 1, axis=1)]
                df.reset_index(drop=True, inplace=True)
                # Print the formatted table
                df.columns=column_names
                print(tabulate(df, headers='keys', tablefmt="grid"))
                print('length of the previous df:\t',len(df))
                dfs.append(df)
                print(len(dfs))
                # print(tabulate(old_df, headers='keys', tablefmt="grid"))
            except Exception as e:
                try:            
                    tables = camelot.read_pdf(file_path, pages=str(k+1), flavor='stream')
                    
                    # Get the first table
                    table = tables[0].df
                    
                    # Process the DataFrame to handle multi-line cells
                    processed_data = []
                    for i, row in table.iterrows():
                        if i == 0:  # Skip header row
                            headers = row.tolist()
                            processed_data.append(headers)
                        else:
                            # Combine multi-line cells in the 'Description' column
                            if pd.isna(row[0]):
                                processed_data[-1][1] += ' ' + ' '.join(row.dropna().tolist())
                            else:
                                processed_data.append(row.tolist())
                    
                    # Convert the processed data to a DataFrame
                    final_df = pd.DataFrame(processed_data[1:], columns=processed_data[0])
                    
                    for idx, row in final_df.iterrows():
                            if idx > 1:
                                if all((cell == '' or pd.isnull(cell)) for col, cell in row.items() if col != final_df.columns[1]):
                                    if final_df.at[idx,final_df.columns[1]] not in strings_to_drop:
                                        final_df.at[idx-1,final_df.columns[1]]=str(final_df.at[idx-1,final_df.columns[1]])+' '+str(final_df.at[idx,final_df.columns[1]])
                    
                    
                    final_df = final_df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
                    
                    # Remove rows with empty cells or empty strings in the first column
                    final_df = final_df[~final_df[final_df.columns[0]].isin(['', ' '])]
                    
                    # Remove rows where the first column is not a number
                    final_df = final_df[final_df[final_df.columns[0]].notna() | final_df[final_df.columns[0]].shift().notna()]
                    final_df = final_df[pd.to_numeric(final_df[final_df.columns[0]], errors='coerce').notna()]
                    
                    # Remove columns that are empty or full of spaces/empty strings
                    final_df = final_df.dropna(axis=1, how='all')
                    final_df = final_df.drop(columns=[col for col in final_df.columns if final_df[col].isin(['', ' ']).all()])
                    
                    # Merge rows with only the second cell non-empty
                    
                    
                    # Remove rows with only one non-empty cell
                    final_df[final_df.columns[0]] = final_df[final_df.columns[0]].fillna(method='ffill')
                    final_df[final_df.columns[1]] = final_df[final_df.columns[1]].fillna(method='ffill')
                    dfs.append(final_df)
                except :
                    print(e)
                    pass
            print(len(dfs))
            concatenated_df = pd.concat(dfs, ignore_index=True)
            
            concatenated_df[concatenated_df.columns[2]] = concatenated_df[concatenated_df.columns[2]].str.extract(r'(\d+)')
            concatenated_df[concatenated_df.columns[3]] = concatenated_df[concatenated_df.columns[3]].str.extract(r'(\d+)')
            concatenated_df[concatenated_df.columns[4]] = concatenated_df[concatenated_df.columns[4]].str.extract(r'\$(\d+\.\d+)')
            index_to_delete = concatenated_df[concatenated_df[concatenated_df.columns[0]] == 'Forgotten something?'].index
            
            if not index_to_delete.empty:
                # If the value is found, get the index of the first occurrence
                index_to_delete = index_to_delete[0]
                
                # Delete the row containing the value and all rows that come after it
                concatenated_df= concatenated_df.iloc[:index_to_delete]
            print(tabulate(concatenated_df, headers='keys', tablefmt="grid"))

            filtered_df = concatenated_df
            print(tabulate(filtered_df, headers='keys', tablefmt="grid"))
            # except Exception as e:
            #     print(traceback.format_exc())
            #     pass
            # print(indexes_not_to_drop)
            
                
            
            filtered_df.reset_index(drop=True, inplace=True)
            # print(tabulate(filtered_df, headers='keys', tablefmt="grid"))
            print(len(filtered_df))
            
            print(tabulate(filtered_df, headers='keys', tablefmt="grid"))
            # print(concatenated_df.iloc[0])
            try:
                filtered_df.to_excel(f'{first_path}/{file_name}__extracted_tables_with_camelot.xlsx',index=False)
                
                youlocation_file.value  = f"Tables are ready. Please check: \"{first_path}\""
                youlocation_file.update()
            except Exception as e :
                youlocation_file.value  = e
                youlocation_file.update()
                print(traceback.format_exc())

def main(page:ft.Page):

    youlocation_file = ft.Text("")


    def dialog_picker(e:ft.FilePickerResultEvent):
        for x in e.files:   

            # shutil.copy(x.name,f"myUploads/{x.name}")
            
            # 			# SET LOCATION FOLDER IMAGE
            youlocation_file.value = x.path
            youlocation_file.update()
            file_path  = r'{}'.format(x.path)
            extract_tables_from_pdf(x.name,file_path,youlocation_file)





    Mypick = ft.FilePicker(on_result=dialog_picker)
    page.overlay.append(Mypick)


    page.add(
        ft.Row([ft.Column([ft.ElevatedButton("Insert file",on_click=lambda _: Mypick.pick_files()),youlocation_file],alignment=ft.MainAxisAlignment.CENTER)],alignment=ft.MainAxisAlignment.CENTER),
		
		)

ft.app(target=main)
