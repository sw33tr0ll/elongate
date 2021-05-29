import { Component, Input, OnInit } from '@angular/core';
import {FormBuilder, FormGroup, FormControl, Validators} from '@angular/forms';
import { ReactiveFormsModule } from '@angular/forms';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  form: FormGroup = new FormGroup({});
  title: string;
  api_response: any;
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
      this.api_response = data;
      console.log(this.api_response);
    }, err => console.error(err), () => console.log('Finished Loading...'));
  }
}
