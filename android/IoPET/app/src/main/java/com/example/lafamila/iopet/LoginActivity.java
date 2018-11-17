package com.example.lafamila.iopet;

import android.content.Intent;
import android.os.AsyncTask;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.message.BasicNameValuePair;
import org.apache.http.util.EntityUtils;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class LoginActivity extends AppCompatActivity {
    EditText pet;
    Button go;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);
        pet = (EditText)findViewById(R.id.petID);
        go = (Button)findViewById(R.id.goChat);
        go.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                (new MyAsyncTask()).execute(pet.getText().toString());
            }
        });
    }

    private class MyAsyncTask extends AsyncTask<String, Integer, Integer> {

        @Override
        protected Integer doInBackground(String... params) {

            return postData(params[0]);
        }

        protected void onPostExecute(Integer result) {
            Log.d("status", result.toString());
            if(result != -1){
                Intent intent = new Intent(getBaseContext(), MainActivity.class);
                intent.putExtra("room_id", result);
                startActivity(intent);
            }
        }


        public Integer postData(String valueIWantToSend) {
            // Create a new HttpClient and Post Header
            Integer result = -1;
            HttpClient httpclient = new DefaultHttpClient();
            HttpPost httppost = new HttpPost(
                    "http://13.125.255.139:5000/petLogin");

            try {
                // Add your data
                List<NameValuePair> nameValuePairs = new ArrayList<NameValuePair>();
                nameValuePairs.add(new BasicNameValuePair("pet_id",
                        valueIWantToSend));
                httppost.setEntity(new UrlEncodedFormEntity(nameValuePairs));

                // Execute HTTP Post Request
                HttpResponse response = httpclient.execute(httppost);
                result = response.getStatusLine().getStatusCode();

                if(result == 200){
                    HttpEntity entity = response.getEntity();
                    String responseString = EntityUtils.toString(entity, "UTF-8");
                    return Integer.parseInt(responseString);
                }
                else{
                    return -1;

                }

            } catch (ClientProtocolException e) {
                // TODO Auto-generated catch block
            } catch (IOException e) {
                // TODO Auto-generated catch block
            }
            return result;
        }
    }
}
