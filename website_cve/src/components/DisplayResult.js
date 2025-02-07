//import api from "./api";
import React, { Component } from 'react'
import ListBox from './ListBox'
import DisplayCve from './DisplayCve';
import Spinner from './Spinner';

export default class DisplayResult extends Component {
  constructor(props){
    super(props);
    this.allWebsites = ["Wappalyzer", "BuiltWith", "WhatRuns", "W3Techs"];
    this.state = {
      cve_dict: '',
      loading: false,
    }
    // let {scrapedDepObj} = this.props;
  }
  s;

  handleCVEOnlcick = async () =>{
    console.log(JSON.stringify({"final_list":this.props.scrapedDepObj.final_list}))

    this.setState({loading: true})
    let data = await fetch("http://127.0.0.1:8000/getcve",{
      method : "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({"final_list":this.props.scrapedDepObj.final_list})
    })

    let parsedData = await data.json()

    this.setState({cve_dict: parsedData})
    this.setState({loading: false})
    // console.log(parsedData)
  }

  render() {
    
    if(this.props.scrapedDepObj.Exist === true){
      const dispAllWebsites = []
      this.allWebsites.forEach((website) => {
        dispAllWebsites.push(<ListBox title={website} depList={this.props.scrapedDepObj[website]} />)
      })
      return(
        <>
          {dispAllWebsites}
          {
            this.state.cve_dict ? <DisplayCve cve_dict={this.state.cve_dict}/> : <button className="btn btn-primary my-2" onClick={this.handleCVEOnlcick}>Fetch CVEs</button>
          }
          {this.state.loading ? <Spinner/> : null}
        </>
        
      )
    }
    else{
      return(
        <><p>Website does not exist</p></>
      )
    }
  }
}


// export default function DisplayResult(props){

//   const allWebsites = ["Wappalyzer", "BuiltWith", "WhatRuns", "W3Techs"]

//   if(props.scrapedDepObj.Exist === true){
//     const dispAllWebsites = []
//     allWebsites.forEach((website) => {
//       dispAllWebsites.push(<ListBox title={website} depList={props.scrapedDepObj[website]} />)
//     })
//     return(
//       <>
//         {dispAllWebsites}
//         <button className="btn btn-primary my-2">Fetch CVEs</button>
//       </>
      
//     )
//   }
//   else{
//     return(
//       <><p>Website does not exist</p></>
//     )
//   }
// }

// function ListBox({title, depList}){
    
//     const joinIdividualList = depList.map((dep) => dep.join(' '));
//     console.log(joinIdividualList)
  
//     const styledList = []

//     if(joinIdividualList.length === 0){
//       styledList.push(<span className='border border-secondary m-1 p-1'>No Dependency Found</span>)
//     }
//     else{
//       joinIdividualList.forEach(element => {
//         styledList.push(<span className='border border-secondary m-1 p-1'>{element}</span>)
//       });
//     }
    
    
//     return (
//       <>
//       <div className="container my-3">
//         <h2>{title}</h2>
//         <div className="container d-flex flex-wrap" style={{width:900}}>
//             {styledList}
//         </div>
//       </div>
//       </>
//     )
// }
