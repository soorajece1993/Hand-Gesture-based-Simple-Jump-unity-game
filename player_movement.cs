using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;
// using System.Collections;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;

public class player_movement : MonoBehaviour
{
    // Start is called before the first frame update
    Thread receiveThread; //1
	UdpClient client; //2
	int port; //3

	bool inputdata;
    private Rigidbody2D rigidbody2d;
    // public float moveSpeed =5f;
    private void Awake ()
    {
        rigidbody2d=transform.GetComponent<Rigidbody2D>();
    }

    void Start () 
	{
		port = 5065; //1 
		// jump = false; //2 
		InitUDP(); //4
		inputdata=false;
	}

	// 3. InitUDP
	private void InitUDP()
	{
		print ("UDP Initialized");

		receiveThread = new Thread (new ThreadStart(ReceiveData)); //1 
		receiveThread.IsBackground = true; //2
		receiveThread.Start (); //3

	}
	// 4. Receive Data
	private void ReceiveData()
	{
		client = new UdpClient (port); //1
		while (true) //2
		{
			try
			{
				IPEndPoint anyIP = new IPEndPoint(IPAddress.Parse("0.0.0.0"), port); //3
				byte[] data = client.Receive(ref anyIP); //4

				string text = Encoding.UTF8.GetString(data); //5
				print (">> " + text);
				Debug.Log(text);

				// if (text="jump123")
				// {
				// 	Debug.Log(text);
				// 	inputdata=true;
				// }
				inputdata=true;

				// jump = true; //6

			} catch(Exception e)
			{
				print (e.ToString()); //7
			}
		}
	}


    // Update is called once per frame
    void Update()
    { 
    	// Vector3 movement = new Vector3(Input.GetAxis("Horizontal"),0f,0f);
    	// transform.position += movement*Time.deltaTime*moveSpeed;
    	if ( Input.GetKeyDown(KeyCode.Space)){
    		float jumpvelocity = 8f;
    		rigidbody2d.velocity=Vector2.up*jumpvelocity;
    		Debug.Log("Key pressed");
    	}

    	if ( inputdata==true){
    		float jumpvelocity = 8f;
    		rigidbody2d.velocity=Vector2.up*jumpvelocity;

    		Debug.Log("jump");
    		inputdata=false;
    	}


        
    }
}

   
