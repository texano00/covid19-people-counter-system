import { BrowserModule } from '@angular/platform-browser';
import { NgModule, LOCALE_ID } from '@angular/core';

import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import {MatToolbarModule} from '@angular/material/toolbar';
import {MatTableModule} from '@angular/material/table';
import { HttpClientModule } from '@angular/common/http';
import { ChartsModule } from 'ng2-charts';
import { registerLocaleData } from '@angular/common';
import localeITCH from '@angular/common/locales/it-CH';
import { NgxSpinnerModule } from "ngx-spinner";

registerLocaleData(localeITCH);

@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    MatToolbarModule,
    MatTableModule,
    HttpClientModule,
    ChartsModule,
    NgxSpinnerModule
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
