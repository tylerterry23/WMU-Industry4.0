package com.example.rctablet;

import android.app.Activity;
import android.app.Dialog;
import android.content.DialogInterface;
import android.os.AsyncTask;
import android.os.Bundle;

import java.io.DataInputStream;
import java.io.InputStream;
import java.lang.Thread;


import android.graphics.Color;
import android.os.Handler;
import android.view.LayoutInflater;
import android.view.ViewGroup;
import android.view.Window;
import android.widget.AdapterView;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import com.google.android.youtube.player.YouTubeInitializationResult;
import com.google.android.youtube.player.YouTubePlayer;
import com.google.android.youtube.player.YouTubePlayerView;
import com.google.android.youtube.player.YouTubePlayerFragment;
import com.google.android.material.snackbar.Snackbar;

import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;

import android.view.View;

import androidx.fragment.app.FragmentActivity;
import androidx.navigation.NavController;
import androidx.navigation.Navigation;
import androidx.navigation.ui.AppBarConfiguration;
import androidx.navigation.ui.NavigationUI;

import androidx.fragment.app.Fragment;
import androidx.viewpager2.adapter.FragmentStateAdapter;
import androidx.viewpager2.widget.ViewPager2;

import com.example.rctablet.databinding.ActivityMainBinding;

import android.view.Menu;
import android.view.MenuItem;
import android.widget.ArrayAdapter;
import android.widget.Spinner;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;


public class MainActivity extends AppCompatActivity {
    // for popup window
    private AppBarConfiguration appBarConfiguration;
    private ActivityMainBinding binding;
    Dialog myDialog;


    // for timer
    private int seconds = 0;
    private boolean running = false;
    private int avetime = 0;
    private int timeleft;
    String inp;
    private String message;

    //for instruction
    private FragmentStateAdapter pagerAdapter;
    private  int NUM_PAGES = 1;
    private String instr;
    private List<String> instructionlist = new ArrayList<String>();
    private ViewPager2 viewPager;


    //never used -- can probably delete it lol
    YouTubePlayerView youTubePlayerView;
    private AlertDialog.Builder dialogBuilder;
    private AlertDialog dialog;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        binding = ActivityMainBinding.inflate(getLayoutInflater());
        setContentView(binding.getRoot());

        myDialog = new Dialog(this);

        setSupportActionBar(binding.toolbar);

        // for instruction
        instructionlist.add("instruction");
        viewPager = findViewById(R.id.viewpager1);
        pagerAdapter = new ScreenSlidePagerAdapter(MainActivity.this);
        viewPager.setAdapter(pagerAdapter);

        // for toolbar
        NavController navController = Navigation.findNavController(this, R.id.nav_host_fragment_content_main);
        appBarConfiguration = new AppBarConfiguration.Builder(navController.getGraph()).build();
        NavigationUI.setupActionBarWithNavController(this, navController, appBarConfiguration);

        // for button on the bottom for youtube video
        binding.fab.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                youtubeVideo(view);
            }
        });

        // for button at the top for connecting with main application (setting)
        binding.buttonST.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                ShowSettings(view);
            }
        });

        //for sockets
        Thread mythread = new Thread(new myserverthread());
        mythread.start();
        //for timer
        Thread stopwat = new Thread(new stopwatcht());
        stopwat.start();
    }


    //for instruction slides
    //reference https://developer.android.com/develop/ui/views/animations/screen-slide-2#java
    public class ScreenSlidePagerAdapter extends FragmentStateAdapter {
        public ScreenSlidePagerAdapter(FragmentActivity fa) {
            super(fa);
        }

        @Override
        public Fragment createFragment(int posi) {
            //return new ScreenSlidePageFragment();

            Fragment slideitems = new ScreenSlidePageFragment();
            Bundle args = new Bundle();
            int stepnum = posi + 1;
            args.putString(ScreenSlidePageFragment.ARG_OBJECT, "step " + stepnum + "\n\n" + instructionlist.get(posi));
            slideitems.setArguments(args);
            return slideitems;
        }

        @Override
        public int getItemCount() {
            return NUM_PAGES;
        }
    }
    //for instruction slides
    public static class ScreenSlidePageFragment extends Fragment {

        public static final String ARG_OBJECT = "object";
        @Override
        public View onCreateView(LayoutInflater inflater, ViewGroup container,
                                 Bundle savedInstanceState) {
            return (ViewGroup) inflater.inflate(
                    R.layout.for_slide, container, false);
        }
        @Override
        public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
            Bundle args = getArguments();
            ((TextView) view.findViewById(R.id.slidtext))
                    .setText(args.getString(ARG_OBJECT));
        }
    }

    //for timer
    class stopwatcht implements Runnable{
        public void run() {
        runOnUiThread(new Runnable() {
            @Override
            public void run() {
                TextView s_time;
                s_time = (TextView)findViewById(R.id.textView2);
                Handler hand = new Handler();
                hand.post(new Runnable() {
                    @Override

                    public void run() {
                        int minutes = (seconds % 3600) / 60;
                        int secs = seconds % 60;
                        String time
                                = String
                                .format(Locale.getDefault(),
                                        "%02d:%02d",
                                        minutes, secs);

                        // change the color base on how long is left
                        timeleft = avetime - seconds;
                        if(timeleft > 30){
                            s_time.setTextColor(Color.parseColor("#FFADD8E6"));
                        }else if(timeleft <= 30 & timeleft > 20){
                            s_time.setTextColor(Color.parseColor("#FF00008B"));

                        }else if(timeleft <= 20 & timeleft >10){
                            s_time.setTextColor(Color.parseColor("#FF00FF00"));

                        }else if(timeleft <= 10 & timeleft > 0) {
                            s_time.setTextColor(Color.parseColor("#FFFFFF00"));
                        }else{
                            s_time.setTextColor(Color.parseColor("#FFFF0000"));
                        }

                        s_time.setText(time);

                        // If running is true, increment the
                        // seconds variable.
                        if (running) {
                            seconds++;
                        }

                        // Post the code again
                        // with a delay of 1 second.
                        hand.postDelayed(this, 1000);

                        // Format the seconds into hours, m

    }});}});}}

    //for socket connection
    class myserverthread implements Runnable{


        Socket s;
        ServerSocket ss;
        InputStreamReader isr;
        BufferedReader br;
        Handler h = new Handler();
        //String message;

        byte[] bytes = new byte[1024];



        @Override
        public void run() {

            try{
                ss = new ServerSocket(7800);
                while(true){
                    s = ss.accept();
                    //br = new BufferedReader(new InputStreamReader(s.getInputStream()));
                    br = new BufferedReader(new InputStreamReader(s.getInputStream(), StandardCharsets.UTF_8));

                    message = br.readLine();


                    if (running) {
                        running = false;
                    } else {
                        running = true;
                        seconds = 0;
                    }


                    }
            }catch(IOException e){
                e.printStackTrace();
            }
        }
    }



    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
         //Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_main, menu);
        return true;
    }


    @Override
    public boolean onSupportNavigateUp() {
        NavController navController = Navigation.findNavController(this, R.id.nav_host_fragment_content_main);
        return NavigationUI.navigateUp(navController, appBarConfiguration)
                || super.onSupportNavigateUp();
    }

    //for socekt connection
    public class MessageSender extends AsyncTask<String, Void, Void> {

        Socket s;
        DataOutputStream dos;
        PrintWriter pw;
        BufferedReader br;

        @Override
        protected Void doInBackground(String... voids) {

            String message = voids[0];
            try{
                s = new Socket("192.168.1.70", 7800);
                pw = new PrintWriter(s.getOutputStream());
                br = new BufferedReader(new InputStreamReader(s.getInputStream(), StandardCharsets.UTF_8));
                pw.write(message);
                pw.flush();

                inp = br.readLine();

                avetime = Integer.parseInt(inp);
                NUM_PAGES = 0;
                instructionlist.clear();


                while (1 == 1){
                    instr = br.readLine();
                    if(instr == null){
                        break;
                    }
                    instructionlist.add(instr);
                    NUM_PAGES++;

                }

                pw.close();
                br.close();
                s.close();
            }catch(IOException e){
                e.printStackTrace();
            }

            return null;
        }
    }


    public void ShowSettings(View V) {
        TextView txtclose;
        Button apbutton;
        Button clbutton;
        myDialog.setContentView(R.layout.fragment_settings);

        txtclose = (TextView) myDialog.findViewById(R.id.textView8);
        apbutton = (Button) myDialog.findViewById(R.id.applybutton);
        clbutton = (Button) myDialog.findViewById(R.id.closebutton);
        Spinner dropdown = myDialog.findViewById(R.id.spinner);
        String[] items = new String[]{"Station 1","Station 2","Station 3","Station 4","Station 5"};
        ArrayAdapter<String> adapter = new ArrayAdapter<String>(this, R.layout.for_spinner, items);
        adapter.setDropDownViewResource(R.layout.for_spinner);
        dropdown.setAdapter(adapter);
        TextView avtime = (TextView) findViewById(R.id.textView);
        TextView station_number = (TextView) findViewById(R.id.textView7);
        TextView spent_time = (TextView) findViewById(R.id.textView2);
        apbutton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                int stationnumber = dropdown.getSelectedItemPosition();
                MessageSender messagesender = new MessageSender();
                switch (stationnumber){
                    case 0:
                        station_number.setText("Station 1");
                        break;
                    case 1:
                        station_number.setText("Station 2");
                        break;
                    case 2:
                        station_number.setText("Station 3");
                        break;
                    case 3:
                        station_number.setText("Station 4");
                        break;
                    case 4:
                        station_number.setText("Station 5");
                        break;

                }
                messagesender.execute(station_number.getText().toString());
                try {
                    Thread.sleep(500);
                } catch (InterruptedException e) {
                    throw new RuntimeException(e);
                }
                spent_time.setText("00:00");
                int minutesav = ( avetime % 3600) / 60;
                int secsav = avetime % 60;
                String timeave
                        = String
                        .format(Locale.getDefault(),
                                "%02d:%02d",
                                minutesav, secsav);
                avtime.setText(timeave);
                viewPager = findViewById(R.id.viewpager1);
                pagerAdapter = new ScreenSlidePagerAdapter(MainActivity.this);
                viewPager.setAdapter(pagerAdapter);
                seconds = 0;
                running = false;
                myDialog.dismiss();


            }
        });
        clbutton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View V) {
                myDialog.dismiss();
            }
        });
        myDialog.show();
        Window window = myDialog.getWindow();
        window.setLayout(700,800);
        myDialog.setCancelable(false);
        myDialog.setCanceledOnTouchOutside(false);
    }

    // play youtube video
    public void youtubeVideo(View V){
        TextView txtclose;
        String api_key = "AIzaSyCElofuQDQdNNfSmyJHKeaf32zfhb8nTak";

        myDialog.setContentView(R.layout.popup);
        //YouTubePlayerView ytPlayer = (YouTubePlayerView) myDialog.findViewById(R.id.ytPlayer);
        YouTubePlayerFragment ytPlayer = (YouTubePlayerFragment) getFragmentManager().findFragmentById(R.id.ytPlayer);

        ytPlayer.initialize(
                api_key,
                new YouTubePlayer.OnInitializedListener() {
                    @Override
                    public void onInitializationSuccess(
                            YouTubePlayer.Provider provider,
                            YouTubePlayer youTubePlayer, boolean b) {
                        youTubePlayer.loadVideo("b9mJrzdlfR8");
                        youTubePlayer.play();
                    }
                    @Override
                    public void onInitializationFailure(YouTubePlayer.Provider provider,
                                                        YouTubeInitializationResult
                                                                youTubeInitializationResult) {
                        Toast.makeText(getApplicationContext(), "Video player Failed", Toast.LENGTH_SHORT).show();
                    }
                });
        txtclose = (TextView) myDialog.findViewById(R.id.textView5);
        txtclose.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View V) {

                getFragmentManager().beginTransaction().remove(ytPlayer).commit();
                myDialog.dismiss();
            }
        });
        myDialog.show();
        Window window = myDialog.getWindow();
        window.setLayout(750,600);
        myDialog.setCancelable(false);
        myDialog.setCanceledOnTouchOutside(false);




    }

}