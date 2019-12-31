import { Component, OnInit } from '@angular/core';
import { HttpClientModule, HttpClient } from '@angular/common/http';
import { FormGroup, FormControl, ReactiveFormsModule } from '@angular/forms';

@Component({
  selector: 'app-add-pdf',
  templateUrl: './add-pdf.component.html',
  styleUrls: ['./add-pdf.component.css']
})
export class AddPdfComponent implements OnInit {
  columnDefs: any;
  rowData: any;

  profileForm = new FormGroup({
    firstName: new FormControl(''),
    lastName: new FormControl(''),
    image: new FormControl('')
  });
  title = 'helloworld';
  fileData = null;
  data:any[];
  startval:number;



  // settings: any;

  constructor(private http: HttpClient) { }

  ngOnInit() {
    this.startval=0
    console.log('im heheh');
  }

  fileProgress(fileInput: any) {
    this.fileData = <File>fileInput.target.files[0];
  }

  onSubmit() {
    console.log('im her66666e');
    // const formData = new FormData();
    // formData.append('file', this.fileData);
    console.log(this.profileForm.value);


    console.log('im he44444re');
    // this.http.post('http://127.0.0.1:8000/', formData)
    //   .subscribe(res => {
    //     console.log(res);
    //     alert('SUCCESS !!');
    //   })
    let obj = JSON.parse(this.profileForm.value.image);
    console.log(obj);

    // this.data=['first_Name', 'last_Name', 'DOB', 'school_code', 'test_date', 'test_code'];

    this.data=[];
    let outCheck = []
    for (var key in obj) {
      if (obj.hasOwnProperty(key)) {
        let temp={first_Name: obj[key].first_Name, last_Name:obj[key].last_Name, DOB:obj[key].DOB,
          school_code:obj[key].school_code, test_date:obj[key].test_date, test_code:obj[key].test_code};


          this.data.push(temp);

        }
    }


      this.startval = 1;
      // this.settings={
      //   data: this.data,
      //   rowHeaders: true,
      //   colHeaders: true,

      //   width=1000,
      //   height=1500,


      //   licenseKey: 'non-commercial-and-evaluation'
    }
}

