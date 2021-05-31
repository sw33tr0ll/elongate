import { Component, Input, OnInit } from '@angular/core';
import {FormBuilder, FormGroup, FormControl, Validators} from '@angular/forms';
import { ReactiveFormsModule } from '@angular/forms';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { AnalysisResponse } from './models/AnalysisResponse';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  form: FormGroup = new FormGroup({});
  title: string;
  single_analysis: any;
  recent_tweets: any;
  constructor(private fb: FormBuilder, private http: HttpClient) { }

  ngOnInit(): void {
    const reg = /^https?:\/\/twitter\.com\/(?:#!\/)?(\w+)\/status(es)?\/(\d+)/;
    this.form = this.fb.group({
      tweet: ['', [Validators.required, Validators.pattern(reg)]]
    });
    this.title = 'elongate';
  }
  get f() {
    return this.form.controls;
  }
  submit() {
    const tweet_url = this.form.value.tweet;
    console.log(tweet_url);
    this.http.post('https://elongate-api.loganevans.me/prod/analyze',{'tweet': tweet_url}).subscribe(data => {
      this.single_analysis = JSON.stringify(data).replace(/([{},:])/g, ' $1 ');
      console.log(this.single_analysis);
    }, err => console.error(err), () => console.log('Finished Loading...'));
  }
  seeRecent() {
    this.http.get('https://elongate-api.loganevans.me/prod/recent').subscribe(data => {
      this.recent_tweets = JSON.stringify(data).replace(/([{},:])/g, ' $1 ');
      console.log(this.recent_tweets);
    }, err => console.error(err), () => console.log('Finished Loading...'));
  }
}
