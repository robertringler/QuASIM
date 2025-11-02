"""IR builder for constructing QuASIM intermediate representation."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, List, Optional


class IRType(Enum):
    """Supported IR tensor types."""
    FP32 = "fp32"
    FP16 = "fp16"
    FP8 = "fp8"
    INT4 = "int4"
    INT8 = "int8"
    COMPLEX64 = "complex64"
    COMPLEX128 = "complex128"


@dataclass
class IRNode:
    """Represents a node in the IR computation graph."""
    op: str
    inputs: List[IRNode] = field(default_factory=list)
    outputs: List[IRNode] = field(default_factory=list)
    dtype: IRType = IRType.FP32
    shape: tuple[int, ...] = field(default_factory=tuple)
    metadata: dict[str, Any] = field(default_factory=dict)
    
    def __hash__(self) -> int:
        return id(self)


class IRBuilder:
    """Builder for constructing IR computation graphs."""
    
    def __init__(self) -> None:
        self.nodes: List[IRNode] = []
        self._fusion_enabled = True
        
    def add_tensor_op(
        self,
        op: str,
        inputs: List[IRNode],
        dtype: IRType = IRType.FP32,
        shape: tuple[int, ...] = (),
        metadata: Optional[dict[str, Any]] = None,
    ) -> IRNode:
        """Add a tensor operation to the IR graph."""
        node = IRNode(
            op=op,
            inputs=inputs,
            dtype=dtype,
            shape=shape,
            metadata=metadata or {},
        )
        self.nodes.append(node)
        for inp in inputs:
            inp.outputs.append(node)
        return node
    
    def enable_fusion(self, enable: bool = True) -> None:
        """Enable or disable graph-level fusion optimization."""
        self._fusion_enabled = enable
        
    def optimize(self) -> None:
        """Apply optimization passes to the IR graph."""
        if self._fusion_enabled:
            self._fuse_elementwise_ops()
            
    def _fuse_elementwise_ops(self) -> None:
        """Fuse consecutive elementwise operations."""
        fusable_ops = {"add", "mul", "sub", "div", "relu", "tanh"}
        fused_nodes: List[IRNode] = []
        replaced = set()

        for node in self.nodes:
            # Skip nodes that have already been fused
            if node in replaced:
                continue
            if node.op in fusable_ops and len(node.inputs) == 1:
                parent = node.inputs[0]
                if (
                    parent.op in fusable_ops
                    and len(parent.outputs) == 1
                    and parent not in replaced
                ):
                    # Create a new fused node
                    fused_op = f"{parent.op}_{node.op}"
                    fused_metadata = dict(parent.metadata)
                    fused_metadata.update(node.metadata)
                    fused_metadata["fused_from"] = [parent.op, node.op]
                    fused_node = IRNode(
                        op=fused_op,
                        inputs=parent.inputs,
                        dtype=node.dtype,
                        shape=node.shape,
                        metadata=fused_metadata,
                    )
                    # Update outputs of parent.inputs to point to fused_node
                    for inp in parent.inputs:
                        inp.outputs = [
                            fused_node if out is parent else out for out in inp.outputs
                        ]
                    # Update outputs of fused_node
                    fused_node.outputs = node.outputs.copy()
                    # Update inputs of node.outputs to point to fused_node
                    for out in node.outputs:
                        out.inputs = [
                            fused_node if inp is node else inp for inp in out.inputs
                        ]
                    fused_nodes.append(fused_node)
                    replaced.add(parent)
                    replaced.add(node)
                    continue
            fused_nodes.append(node)
        self.nodes = fused_nodes
        
    def to_mlir(self) -> str:
        """Export IR graph to MLIR format."""
        lines = ["module {"]
        for idx, node in enumerate(self.nodes):
            dtype_str = node.dtype.value
            shape_str = "x".join(map(str, node.shape)) if node.shape else "scalar"
            inputs_str = ", ".join(f"%{i}" for i in range(len(node.inputs)))
            lines.append(f"  %{idx} = {node.op}({inputs_str}) : tensor<{shape_str}x{dtype_str}>")
        lines.append("}")
        return "\n".join(lines)
