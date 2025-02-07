import React, { useState } from 'react';

const DisplayCve = ({ cve_dict }) => {
    const [expanded, setExpanded] = useState({});

    const toggleExpand = (key) => {
        setExpanded(prevState => ({
            ...prevState,
            [key]: !prevState[key]
        }));
    };

    return (
        <div className="container">
            <h1>CVEs</h1>
            {Object.keys(cve_dict).map((key, index) => {
                return (
                    <div key={index}>
                        <h2>{key}</h2>
                        {cve_dict[key].map((cve_list, index) => {
                            return (
                                <div key={index}>
                                    {cve_list.map((cve, index) => {
                                        return (
                                            <div key={index} className="row border-bottom py-2 align-items-center">
                                                <div className="col-md-3">{cve['ID']}</div>
                                                <div className="col-md-6">
                                                    <button
                                                        className="btn btn-link"
                                                        onClick={() => toggleExpand(cve['ID'])}
                                                        aria-controls={`collapse-${cve['ID']}`}
                                                        aria-expanded={expanded[cve['ID']]}
                                                    >
                                                        {expanded[cve['ID']] ? 'Hide Description' : 'Show Description'}
                                                    </button>
                                                    <div className={`collapse ${expanded[cve['ID']] ? 'show' : ''}`} id={`collapse-${cve['ID']}`}>
                                                        <p>{cve['Description']}</p>
                                                    </div>
                                                </div>
                                                <div className="col-md-3">
                                                    <p>Cvss3: {cve['Cvss3']}</p>
                                                    <p>Cvss2: {cve['Cvss2']}</p>
                                                </div>
                                            </div>
                                        )
                                    })}
                                </div>
                            )
                        })}
                    </div>
                )
            })}
        </div>
    )
}

export default DisplayCve;