package com.example.lafamila.iopet;

import android.content.Intent;
import android.os.AsyncTask;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ListView;


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
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.net.URISyntaxException;
import java.util.ArrayList;
import java.util.List;

import com.github.nkzawa.socketio.client.IO;
import com.github.nkzawa.socketio.client.Socket;
import com.github.nkzawa.emitter.Emitter;

public class MainActivity extends AppCompatActivity {
    ListView m_ListView;
    CustomAdapter m_Adapter;
    private Socket mSocket;
    EditText edit;
    int room_id;
    private Emitter.Listener onNewMessage = new Emitter.Listener() {
        JSONObject arg;
        String sender = "";
        String msg = "";
        boolean isImage = false;
        @Override
        public void call(Object... args) {
            arg = (JSONObject) args[0];
            try{
                sender = arg.getString("sender");
                msg = arg.getString("message");
                isImage = !arg.getString("type").equals("text");
                Log.d("messageRecieved", msg);
                Log.d("messageSender", sender);

            } catch (JSONException e) {
                return;
            }
            if(sender.equals("hospt")){
                Log.d("messageRecieved", msg);
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {

                        m_Adapter.add(msg, 0, isImage);
                        m_ListView.setAdapter(m_Adapter);
                        // add the message to view
                    }
                });

            }

        }
    };
//    private Emitter.Listener onMessageReceived = new Emitter.Listener() {
//        @Override
//        public void call(Object... args) {
//            JSONObject receivedData = (JSONObject) args[0];
//            try{
//                Log.d("message",receivedData.getString("message"));
//                ((CustomAdapter)m_ListView.getAdapter()).add(receivedData.getString("message"), 0);
//                m_ListView.clearFocus();
//                edit.requestFocus();
//                m_ListView.requestFocus();
//            }catch (JSONException e){
//                e.printStackTrace();
//            }
//        }
//    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Intent intent = getIntent();
        room_id = intent.getIntExtra("room_id", -1);


        try{
            mSocket = IO.socket("http://13.125.255.139:5000");
            JSONObject object = new JSONObject();
            try{
                object.put("room_id", room_id);
                object.put("sender", "pet");
            }catch (JSONException e){
                e.printStackTrace();
            }

            mSocket.connect();
            mSocket.emit("join", object);
            mSocket.on("received", onNewMessage);
            //m_Adapter.add("New User", 2);
        }catch (URISyntaxException e){
            e.printStackTrace();
        }



        (new MyAsyncTask()).execute(""+room_id);

        edit = (EditText)findViewById(R.id.editText1);
        m_Adapter = new CustomAdapter();
        m_ListView = (ListView) findViewById(R.id.listView1);

        m_ListView.setAdapter(m_Adapter);




        Button send = (Button)findViewById(R.id.button1);
        send.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                String txt = edit.getText().toString();
                edit.setText("");

                m_Adapter.add(txt, 1, false);
                //이미지를 업로드하는경우
                //m_Adapter.add(업로드된 파일 경로, 1, true);
                m_ListView.setAdapter(m_Adapter);
                edit.requestFocus();
                m_ListView.requestFocus();
                JSONObject object = new JSONObject();
                try{
                    object.put("message", txt);
                    object.put("type", "text");
                    object.put("room_id", room_id);
                    object.put("sender", "pet");
                }catch (JSONException e){
                    e.printStackTrace();
                }
                mSocket.emit("message", object);
            }
        });





    }

    @Override
    public void onDestroy() {
        super.onDestroy();
        JSONObject object = new JSONObject();
        try{
            object.put("room_id", room_id);
        }catch (JSONException e){
            e.printStackTrace();
        }
        mSocket.emit("leave", object);
        mSocket.disconnect();
        mSocket.off("message", onNewMessage);
    }



    private class MyAsyncTask extends AsyncTask<String, Integer, JSONArray> {

        @Override
        protected JSONArray doInBackground(String... params) {
            // TODO Auto-generated method stub

            return postData(params[0]);
        }

        protected void onPostExecute(JSONArray result) {
            Log.d("status", result.toString());
            for (int i = 0; i < result.length(); i++) { // Walk through the Array.
                try{
                    JSONObject obj = result.getJSONObject(i);

                    m_Adapter.add(obj.getString("CHAT_MESSAGE"), obj.getInt("CHAT_SEND"), obj.getInt("CHAT_TYPE")==1);
                }catch (JSONException e){
                    e.printStackTrace();
                }
                m_ListView.setAdapter(m_Adapter);
                // Do whatever.
            }
        }


        public JSONArray postData(String valueIWantToSend) {
            // Create a new HttpClient and Post Header
            Integer result = -1;
            HttpClient httpclient = new DefaultHttpClient();
            HttpPost httppost = new HttpPost(
                    "http://13.125.255.139:5000/chatList");
            //            "http://13.125.255.139:5000/chatList");

            try {
                // Add your data
                List<NameValuePair> nameValuePairs = new ArrayList<NameValuePair>();
                nameValuePairs.add(new BasicNameValuePair("room_id",
                        valueIWantToSend));
                httppost.setEntity(new UrlEncodedFormEntity(nameValuePairs));

                // Execute HTTP Post Request
                HttpResponse response = httpclient.execute(httppost);
                result = response.getStatusLine().getStatusCode();

                if(result == 200){
                    HttpEntity entity = response.getEntity();
                    String responseString = EntityUtils.toString(entity, "UTF-8");
                    try{
                        return new JSONArray(responseString);
                    }catch (JSONException e){
                        e.printStackTrace();
                    }
                }
                else{
                    return new JSONArray();

                }

            } catch (ClientProtocolException e) {
                // TODO Auto-generated catch block
            } catch (IOException e) {
                // TODO Auto-generated catch block
            }
            return new JSONArray();
        }
    }
}
