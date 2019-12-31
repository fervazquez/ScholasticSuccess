import { ReactiveFormsModule} from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { AddPdfComponent } from './add-pdf/add-pdf.component';
import { HotTableModule } from '@handsontable/angular';
import { AgGridModule } from 'ag-grid-angular';


@NgModule({
  declarations: [
    AppComponent,
    AddPdfComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    ReactiveFormsModule,
    HotTableModule.forRoot(),
    AgGridModule.withComponents([])
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
