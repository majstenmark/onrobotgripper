import java.util.*;
import java.io.*;
import java.net.*;
import java.nio.*;

public class GripperCom{
    
    private String HOST = "localhost";
    private int PORT = 30000;
    private int timeout_ms = 10000;
    private Socket socket;
    private OutputStream output;
    private  BufferedReader input;

    public static void main(String[] args){
       GripperCom gripper = new GripperCom("192.168.1.163");
       gripper.connect();
       
       System.out.println("Open ...");
       gripper.open();
       
       System.out.println("Close ...");
       System.out.println(gripper.close());
       
       System.out.println("Moving to position");
       gripper.moveto(20, 35, 20);
       
       System.out.println("Open ...");
       gripper.open();
       System.out.println("Current position ...");
       System.out.println(gripper.getPosition());
       System.out.println("Close ...");
       System.out.println(gripper.close());
       
    }

    public GripperCom(String ip){
        HOST = ip;
    }

    private void connect(){
        try{
        socket = new Socket(); 
        SocketAddress socketAddress = new InetSocketAddress(HOST, PORT); 
        socket.connect(socketAddress, timeout_ms);
        output = socket.getOutputStream();
        input =  new BufferedReader(new InputStreamReader(socket.getInputStream()));
        }catch(IOException ex){
            System.out.println(ex.getMessage());
        }

    }

    private String send(String msg){
        try{
        byte[] data = msg.getBytes("UTF-8");
        output.write(data);
        output.flush();
        String line = input.readLine();
        System.out.println("Got "+  line);
        return line;

        }catch(IOException ex){
            System.out.println(ex.getMessage());
            return "error";
        }

        
    }

    private void open(){
        send("open");
    }

    private boolean close(){
        String response = send("close");
        return response.equals("gripdetected");

    }

    private void moveto(int w, int force, int speed){
        String msg = "moveto " + w + " " + force + " " + speed;
        send(msg);
    }

    private double getPosition(){
        String value = send("getposition");
        return Double.parseDouble(value);
    }

    

}