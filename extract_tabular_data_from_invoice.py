import os
import re
import traceback
from typing import List

import camelot
import flet as ft
import pandas as pd
import pdfplumber
from tabulate import tabulate

def create_output_directory(file_name: str) -> str:
    os.makedirs('output', exist_ok=True)
    first_path = f'output/{file_name}'
    os.makedirs(first_path, exist_ok=True)
    return first_path

def process_dataframe(df: pd.DataFrame, strings_to_drop: List[str]) -> pd.DataFrame:
    for idx, row in df.iterrows():
        if idx > 1:
            if all((cell == '' or pd.isnull(cell)) for col, cell in row.items() if col != df.columns[1]):
                if df.at[idx,df.columns[1]] not in strings_to_drop:
                    df.at[idx-1,df.columns[1]]=str(df.at[idx-1,df.columns[1]])+' '+str(df.at[idx,df.columns[1]])
    df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    
    # If there are 7 columns and the second column is mostly empty, drop it
    if len(df.columns) == 7:
        second_column = df.iloc[:, 1]
        if second_column.isna().sum() / len(second_column) > 0.8 or (second_column == '').sum() / len(second_column) > 0.8:
            df = df.drop(df.columns[1], axis=1)
    
    df = df[~df[df.columns[0]].isin(['', ' '])]
    df = df[df[df.columns[0]].notna() | df[df.columns[0]].shift().notna()]
    df = df[pd.to_numeric(df[df.columns[0]], errors='coerce').notna()]
    df = df.dropna(axis=1, how='all')
    df = df.drop(columns=[col for col in df.columns if df[col].isin(['', ' ']).all()])
    
    for idx, row in df.iterrows():
        if idx > 1 and all((cell == '' or pd.isnull(cell)) for col, cell in row.items() if col != df.columns[1]):
            if df.at[idx, df.columns[1]] not in strings_to_drop:
                df.at[idx-1, df.columns[1]] = f"{df.at[idx-1, df.columns[1]]} {df.at[idx, df.columns[1]]}"
    
    df[df.columns[0]] = df[df.columns[0]].fillna(method='ffill')
    df[df.columns[1]] = df[df.columns[1]].fillna(method='ffill')
    return df

def extract_tables_from_pdf(file_name: str, file_path: str, youlocation_file: ft.Text):
    output_path = create_output_directory(file_name)
    pdf = pdfplumber.open(file_path)
    column_names = ['Ref', 'Description', 'Ordered', 'Supplied', 'Unit Price', 'Amount']
    strings_to_drop = [
        'Chocolate, Sweets & Snacks', 'Drinks - Hot & Cold', 'Frozen Foods', 'Liquor - Wine',
        'Bakery', 'Baking & Cooking', '', 'Price $', 'Price', 'Product ID', 'Spices & Seasonings',
        'Jams, Honey & Spreads', 'Condiments & Dressings', 'Canned & Prepared Foods',
        'Baking Supplies & Sugar', 'Biscuits & Crackers', 'Cheese', 'Confectionery', 'Desserts',
        'Laundry', 'Sauces, Stock & Marinades', 'Snack Foods', 'Wine',
        "Here's what was Out of Stock and not supplied",
        "Here's what was substituted and / or modified ", "Unit ",
        "Continued from previous page", 'Cold Drinks', "Here's what was", 'Quant',"Home & Kitchenware"
    ]

    all_dfs = []

    for k in range(len(pdf.pages)):
        print(f' page {k+1} of {len(pdf.pages)}')
        print("=--=" * 5)
        tables = camelot.read_pdf(file_path, pages=str(k+1), flavor='stream')
        
        for table in tables:
            try:
                df = process_dataframe(table.df, strings_to_drop)
                
                # Ensure the dataframe has exactly 6 columns
                if len(df.columns) > 6:
                    df = df.iloc[:, :6]  # Keep only the first 6 columns
                elif len(df.columns) < 6:
                    for i in range(6 - len(df.columns)):
                        df[f'Column_{len(df.columns) + i}'] = ''  # Add empty columns if less than 6
                
                df.columns = column_names  # Now we can safely assign column names
                print(tabulate(df, headers='keys', tablefmt="grid"))
                print('length of the previous df:\t', len(df))
                all_dfs.append(df)
            except Exception as e:
                print(f"Error processing table on page {k+1}: {e}")
                print(traceback.format_exc())

    if all_dfs:
        concatenated_df = pd.concat(all_dfs, ignore_index=True)
        concatenated_df = clean_concatenated_df(concatenated_df)
        
        print(tabulate(concatenated_df, headers='keys', tablefmt="grid"))
        print(f"Total rows: {len(concatenated_df)}")
        
        try:
            excel_path = f'{output_path}/{file_name}_extracted_tables.xlsx'
            concatenated_df.to_excel(excel_path, index=False)
            youlocation_file.value = f"Tables are ready. Please check: {excel_path}"
        except Exception as e:
            youlocation_file.value = f"Error saving Excel file: {str(e)}"
            print(traceback.format_exc())
    else:
        youlocation_file.value = "No tables were successfully extracted from the PDF."
    
    youlocation_file.update()

def clean_concatenated_df(df: pd.DataFrame) -> pd.DataFrame:
    for col in ['Ordered', 'Supplied']:
        df[col] = df[col].str.extract(r'(\d+)')
    df['Unit Price'] = df['Unit Price'].str.extract(r'\$(\d+\.\d+)')
    
    if 'Forgotten something?' in df['Ref'].values:
        df = df.loc[:df[df['Ref'] == 'Forgotten something?'].index[0] - 1]
    
    return df

def main(page: ft.Page):
    youlocation_file = ft.Text("")

    def dialog_picker(e: ft.FilePickerResultEvent):
        if e.files:
            file = e.files[0]
            youlocation_file.value = file.path
            youlocation_file.update()
            extract_tables_from_pdf(file.name, file.path, youlocation_file)

    file_picker = ft.FilePicker(on_result=dialog_picker)
    page.overlay.append(file_picker)

    page.add(
        ft.Row([
            ft.Column([
                ft.ElevatedButton("Insert file", on_click=lambda _: file_picker.pick_files()),
                youlocation_file
            ], alignment=ft.MainAxisAlignment.CENTER)
        ], alignment=ft.MainAxisAlignment.CENTER)
    )

ft.app(target=main)
