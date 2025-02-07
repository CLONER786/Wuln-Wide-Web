import React from 'react'

export default function ListBox({title, depList}){
    
    const joinIdividualList = depList.map((dep) => dep.join(' '));
    console.log(joinIdividualList)
  
    const styledList = []

    if(joinIdividualList.length === 0){
      styledList.push(<span className='border border-secondary m-1 p-1'>No Dependency Found</span>)
    }
    else{
      joinIdividualList.forEach(element => {
        styledList.push(<span key={indexedDB} className='border border-secondary m-1 p-1'>{element}</span>)
      });
    }

    return (
      <>
      <div className="container my-3">
        <h2>{title}</h2>
        <div className="container d-flex flex-wrap" style={{width:900}}>
            {styledList}
        </div>
      </div>
      </>
    )
}

