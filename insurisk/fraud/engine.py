from typing import List, Dict, Any, Set
import networkx as nx
from .schemas import FraudNetworkRequest, FraudClusterResult, FraudInspectionResponse, ClaimEntity

class FraudEngine:
    @staticmethod
    def inspect_network(request: FraudNetworkRequest) -> FraudInspectionResponse:
        # Build bipartite / multi-relational graph using NetworkX
        G = nx.Graph()
        
        claim_map: Dict[str, ClaimEntity] = {}
        
        for claim in request.claims:
            claim_map[claim.claim_id] = claim
            c_node = f"Claim:{claim.claim_id}"
            cl_node = f"Claimant:{claim.claimant_id}"
            pr_node = f"Provider:{claim.provider_id}"
            ad_node = f"Address:{claim.address}"
            
            G.add_node(c_node, type="claim", amount=claim.claim_amount)
            G.add_node(cl_node, type="claimant")
            G.add_node(pr_node, type="provider")
            G.add_node(ad_node, type="address")
            
            G.add_edge(c_node, cl_node, relation="filed_by")
            G.add_edge(c_node, pr_node, relation="treated_by")
            G.add_edge(c_node, ad_node, relation="occurred_at")
            
            if claim.vehicle_vin:
                v_node = f"Vehicle:{claim.vehicle_vin}"
                G.add_node(v_node, type="vehicle")
                G.add_edge(c_node, v_node, relation="involves_vehicle")

        density = float(nx.density(G)) if G.number_of_nodes() > 1 else 0.0
        
        # Find connected components as potential fraud rings
        components = list(nx.connected_components(G))
        high_risk_rings: List[FraudClusterResult] = []
        
        cluster_id = 1
        for comp in components:
            if len(comp) <= 2:
                continue # Ignore trivial components
                
            members = list(comp)
            # Identify shared attributes or high claim concentration
            claims_in_comp = [node for node in members if node.startswith("Claim:")]
            total_amt = sum(claim_map[c.split(":")[1]].claim_amount for c in claims_in_comp if c.split(":")[1] in claim_map)
            
            shared_attrs = []
            evidence = []
            for node in members:
                if not node.startswith("Claim:"):
                    deg = G.degree(node)
                    if deg > 1:
                        shared_attrs.append(f"{node} (Degree: {deg})")
                        evidence.append(
                            f"{node} connects {deg} claims in the same component."
                        )

            if claims_in_comp:
                evidence.append(
                    f"Component contains {len(claims_in_comp)} claims totaling "
                    f"${total_amt:,.2f}."
                )
                        
            # Calculate risk score based on component size, multi-claim density, and amounts
            risk_score = min(100.0, (len(claims_in_comp) * 20.0) + (len(shared_attrs) * 15.0) + (total_amt / 10000.0))
            risk_score = round(risk_score, 2)
            
            if risk_score > 60.0:
                rec = "REFER TO SIU (HIGH PRIORITY COLLUSION RING)"
            elif risk_score > 30.0:
                rec = "FLAG FOR MANUAL AUDIT"
            else:
                rec = "LOW RISK"
                
            high_risk_rings.append(FraudClusterResult(
                cluster_id=cluster_id,
                members=members,
                shared_attributes=shared_attrs,
                risk_score=risk_score,
                recommendation=rec,
                evidence=evidence
            ))
            cluster_id += 1
            
        return FraudInspectionResponse(
            total_claims_analyzed=len(request.claims),
            clusters_detected=len(high_risk_rings),
            high_risk_rings=high_risk_rings,
            network_density=round(density, 4)
        )
