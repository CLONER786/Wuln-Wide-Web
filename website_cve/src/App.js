// import logo from './logo.svg';
import './App.css';
import SearchBar from './components/SearchBar';
//import ListBox from './components/DisplayScraped';
//import DisplayResult from './components/DisplayResult';


// const scrapedDepDict = {
//   "Exist": true,
  
//   "Wappalyzer": [["wordpress","cms","4.9.8"],["wordpress","cms","4.9.8"],["yoast","seo","7.6"],["yoast","seo","7.6"],["requirejs","2.3.6"],["jquery","migrate","3.5.2"],["jquery","3.7.1"],["core-js","3.15.2"],["google","analytics","4"],["microsoft","clarity","0.7.59"],["prebid","6.6.0"],["bidmatic","1.3.4"],["id5","1.0.76"]],

//   "BuiltWith": [["jquery","3.1.1"],["jquery","3.6.3"],["apache","http","server","2.4"],["nginx","1.10"]],

//   "WhatRuns": [["wordpress","cms","4.9.8"],["jquery","3.6.3"],["nginx","1.18.0"],["php","5.5.9"]],

//   "W3Techs": [["jquery","3.6.35"],["requirejs","2.1.14"],["nginx","1.10.3"]],

//   "final_list": [["requirejs","2.1.14"],["jquery","3.1.1"],["nginx","1.10.3"],["wordpress", "cms","4.9.8"],["jquery","migrate","3.5.2"],["jquery","3.6.3"],["yoast","seo","7.6"],["jquery","3.7.1"],["core-js","3.15.2"],["microsoft","clarity","0.7.59"],["nginx","1.10"],["prebid","6.6.0"],["php","5.5.9"],["jquery","3.6.35"],["requirejs","2.3.6"],["nginx","1.18.0"],["id5","1.0.76"],["bidmatic","1.3.4"]]
// }


// function FetchResult({scrapedDepObj}){

//   const allWebsites = ["Wappalyzer", "BuiltWith", "WhatRuns", "W3Techs"]

//   if(scrapedDepObj.Exist === true){
//     const dispAllWebsites = []
//     allWebsites.forEach((website) => {
//       dispAllWebsites.push(<ListBox title={website} depList={scrapedDepDict[website]} />)
//     })
//     return(
//       <>{dispAllWebsites}</>
//     )
//   }
//   else{
//     return(
//       <><p>Website does not exist</p></>
//     )
//   }
// }

function App() {
  
  return (
    <>
    <div className="container">
      <SearchBar searchPlaceholder="Enter Website URL" buttonText="Fetch Dependencies"/>
      {/* <DisplayResult scrapedDepObj={scrapedDepDict}/> */}
    </div>
    </>
  );
}

export default App;
