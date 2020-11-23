/* -- Mode:C++; c-file-style:"gnu"; indent-tabs-mode:nil; -- */
 /*
  * This program is free software; you can redistribute it and/or modify
  * it under the terms of the GNU General Public License version 2 as
  * published by the Free Software Foundation;
  *
  * This program is distributed in the hope that it will be useful,
  * but WITHOUT ANY WARRANTY; without even the implied warranty of
  * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  * GNU General Public License for more details.
  *
  * You should have received a copy of the GNU General Public License
  * along with this program; if not, write to the Free Software
  * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
  *
  */
 #include "ns3/flow-monitor-module.h"
 #include "ns3/flow-monitor-module.h"
 #include "ns3/core-module.h"
 #include "ns3/network-module.h"
 #include "ns3/netanim-module.h"
 #include "ns3/internet-module.h"
 #include "ns3/point-to-point-module.h"
 #include "ns3/applications-module.h"
 #include "ns3/point-to-point-layout-module.h"


 using namespace ns3;

 NS_LOG_COMPONENT_DEFINE ("Star point");
 void
printStats (FlowMonitorHelper &flowmon_helper, bool perFlowInfo) {
  Ptr<Ipv4FlowClassifier> classifier =
DynamicCast<Ipv4FlowClassifier>(flowmon_helper.GetClassifier());
  std::string proto;
  Ptr<FlowMonitor> monitor = flowmon_helper.GetMonitor ();
  std::map < FlowId, FlowMonitor::FlowStats > stats = monitor->GetFlowStats();
  double totalTimeReceiving;
  uint64_t totalPacketsReceived, totalPacketsDropped,
totalBytesReceived,totalPacketsTransmitted;

  totalBytesReceived = 0, totalPacketsDropped = 0,
totalPacketsReceived = 0, totalTimeReceiving =
0,totalPacketsTransmitted = 0;
  for (std::map< FlowId, FlowMonitor::FlowStats>::iterator flow =
stats.begin(); flow != stats.end(); flow++)
  {
    Ipv4FlowClassifier::FiveTuple  t = classifier->FindFlow(flow->first);
    switch(t.protocol)
     {
     case(6):
         proto = "TCP";
         break;
     case(17):
         proto = "UDP";
         break;
     default:
         exit(1);
     }
     totalBytesReceived += (double) flow->second.rxBytes * 8;
     totalTimeReceiving += flow->second.timeLastRxPacket.GetSeconds ();
     totalPacketsReceived += flow->second.rxPackets;
     totalPacketsDropped += flow->second.txPackets - flow->second.rxPackets;
     totalPacketsTransmitted += flow->second.txPackets;
     if (perFlowInfo)
     {
      std::cout << "FlowID: " << flow->first << " (" << proto << " "
                 << t.sourceAddress << " / " << t.sourcePort << " --> "
                 << t.destinationAddress << " / " << t.destinationPort << ")" << std::endl;
       std::cout << "  Tx Bytes: " << flow->second.txBytes << std::endl;
std::cout << "  Lost Packets: " << flow->second.lostPackets << std::endl;
       std::cout << "  Pkt Lost Ratio: " <<((double)flow->second.txPackets-(double)flow->second.rxPackets)/(double)flow->second.txPackets << std::endl;
       std::cout << "  Throughput: " << (((double)flow->second.rxBytes * 8) /(flow->second.timeLastRxPacket.GetSeconds ()) ) << "bits/s" <<std::endl;
       std::cout << "  Mean{Delay}: " <<(flow->second.delaySum.GetSeconds()/flow->second.rxPackets) <<std::endl;
       std::cout << "  Mean{Jitter}: " <<(flow->second.jitterSum.GetSeconds()/(flow->second.rxPackets)) <<std::endl;
     }
}

     std::cout<< "Final throughput with (packets received/total time): "<<(totalBytesReceived)/totalTimeReceiving<<" bps "<<std::endl;
     std::cout<<"Total packets transmitted:"<<totalPacketsTransmitted<<std::endl;
     std::cout<<"Total packets received: "<< totalPacketsReceived<<std::endl;
     std::cout<<"Total packets dropped: "<< totalPacketsDropped<<std::endl;
     std::cout << "Packet Lost Ratio: " << totalPacketsDropped /(double) (totalPacketsReceived + totalPacketsDropped) << std::endl;
}

 int
 main (int argc, char *argv[])
 {

   Config::SetDefault ("ns3::OnOffApplication::PacketSize", UintegerValue (137));

   Config::SetDefault ("ns3::OnOffApplication::DataRate", StringValue ("14kb/s"));

   uint32_t nSpokes = 8;

   CommandLine cmd (__FILE__);
   cmd.AddValue ("nSpokes", "Number of nodes to place in the star", nSpokes);
   cmd.Parse (argc, argv);

   NS_LOG_INFO ("Build star topology.");
   PointToPointHelper pointToPoint;
   pointToPoint.SetDeviceAttribute ("DataRate", StringValue ("5Mbps"));
   pointToPoint.SetChannelAttribute ("Delay", StringValue ("2ms"));
   PointToPointStarHelper star (nSpokes, pointToPoint);

   NS_LOG_INFO ("Install internet stack on all nodes.");
   InternetStackHelper internet;
   star.InstallStack (internet);

   NS_LOG_INFO ("Assign IP Addresses.");
   star.AssignIpv4Addresses (Ipv4AddressHelper ("10.1.1.0", "255.255.255.0"));

   NS_LOG_INFO ("Create applications.");
   
   uint16_t port = 50000;
   Address hubLocalAddress (InetSocketAddress (Ipv4Address::GetAny (), port));
   PacketSinkHelper packetSinkHelper ("ns3::TcpSocketFactory", hubLocalAddress);
   ApplicationContainer hubApp = packetSinkHelper.Install (star.GetHub ());
   hubApp.Start (Seconds (1.0));
   hubApp.Stop (Seconds (10.0));

   OnOffHelper onOffHelper ("ns3::TcpSocketFactory", Address ());
   onOffHelper.SetAttribute ("OnTime", StringValue ("ns3::ConstantRandomVariable[Constant=1]"));
   onOffHelper.SetAttribute ("OffTime", StringValue ("ns3::ConstantRandomVariable[Constant=0]"));

   ApplicationContainer spokeApps;

   for (uint32_t i = 0; i < star.SpokeCount (); ++i)
     {
       AddressValue remoteAddress (InetSocketAddress (star.GetHubIpv4Address (i), port));
       onOffHelper.SetAttribute ("Remote", remoteAddress);
       spokeApps.Add (onOffHelper.Install (star.GetSpokeNode (i)));
     }
   spokeApps.Start (Seconds (1.0));
   spokeApps.Stop (Seconds (10.0));

   NS_LOG_INFO ("Enable static global routing.");
   
   Ipv4GlobalRoutingHelper::PopulateRoutingTables ();

   NS_LOG_INFO ("Enable pcap tracing.");
   
    Ptr<FlowMonitor> flowmon;
    FlowMonitorHelper flowmonHelper;
    flowmon = flowmonHelper.InstallAll ();
    pointToPoint.EnablePcapAll ("star");
  Simulator::Stop (Seconds(10.1));
  Simulator::Run ();

  printStats (flowmonHelper, true);
  Simulator::Destroy ();
   return 0;
 }

