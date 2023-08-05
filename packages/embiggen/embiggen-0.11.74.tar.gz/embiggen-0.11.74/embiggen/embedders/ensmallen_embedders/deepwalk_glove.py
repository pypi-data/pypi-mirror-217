"""Module providing DeepWalk GloVe model implementation."""
from typing import Optional, Dict, Any
from embiggen.embedders.ensmallen_embedders.node2vec import Node2VecEnsmallen

class DeepWalkGloVeEnsmallen(Node2VecEnsmallen):
    """Class providing DeepWalk GloVe implemeted in Rust from Ensmallen."""

    def __init__(
        self,
        embedding_size: int = 100,
        alpha: float = 0.75,
        epochs: int = 100,
        walk_length: int = 512,
        window_size: int = 5,
        max_neighbours: Optional[int] = 100,
        learning_rate: float = 0.05,
        learning_rate_decay: float = 0.99,
        central_nodes_embedding_path: Optional[str] = None,
        contextual_nodes_embedding_path: Optional[str] = None,
        normalize_by_degree: bool = False,
        dtype: str = "f32",
        random_state: int = 42,
        ring_bell: bool = False,
        enable_cache: bool = False,
        verbose: bool = True
    ):
        """Create new abstract DeepWalk method.

        Parameters
        --------------------------
        embedding_size: int = 100
            Dimension of the embedding.
        alpha: float = 0.75
            Alpha parameter for GloVe's loss.
        epochs: int = 100
            Number of epochs to train the model for.
        window_size: int = 10
            Window size for the local context.
            On the borders the window size is trimmed.
        walk_length: int = 512
            Maximal length of the walks.
        window_size: int = 5
            Window size for the local context.
            On the borders the window size is trimmed.
        max_neighbours: Optional[int] = 100
            Number of maximum neighbours to consider when using approximated walks.
            By default, None, we execute exact random walks.
            This is mainly useful for graphs containing nodes with high degrees.
        learning_rate: float = 0.05
            The learning rate to use to train the DeepWalk model. By default 0.01.
        central_nodes_embedding_path: Optional[str] = None
            Path where to mmap and store the central nodes embedding.
            This is necessary to embed large graphs whose embedding will not
            fit into the available main memory.
        contextual_nodes_embedding_path: Optional[str] = None
            Path where to mmap and store the central nodes embedding.
            This is necessary to embed large graphs whose embedding will not
            fit into the available main memory.
        learning_rate_decay: float = 0.99
            Factor to reduce the learning rate for at each epoch. By default 0.9.
        normalize_by_degree: bool = False
            Whether to normalize the random walk by the node degree
            of the destination node degrees.
        dtype: str = "f32"
            The data type to be employed, by default f32.
        random_state: int = 42
            The random state to reproduce the training sequence.
        ring_bell: bool = False,
            Whether to play a sound when embedding completes.
        enable_cache: bool = False
            Whether to enable the cache, that is to
            store the computed embedding.
        verbose: bool = True
            Whether to display the loading bar.
            This will only display the loading bar when
            running the script in a bash-like environment.
            It will not work in Jupyter Notebooks, there
            it will appear in the notebook kernel in some
            systems but not necessarily.
        """
        super().__init__(
            embedding_size=embedding_size,
            alpha=alpha,
            epochs=epochs,
            walk_length=walk_length,
            iterations=1,
            window_size=window_size,
            max_neighbours=max_neighbours,
            learning_rate=learning_rate,
            learning_rate_decay=learning_rate_decay,
            central_nodes_embedding_path=central_nodes_embedding_path,
            contextual_nodes_embedding_path=contextual_nodes_embedding_path,
            normalize_by_degree=normalize_by_degree,
            enable_cache=enable_cache,
            dtype=dtype,
            ring_bell=ring_bell,
            random_state=random_state,
            verbose=verbose,
        )

    def parameters(self) -> Dict[str, Any]:
        """Returns parameters for smoke test."""
        removed = [
            "return_weight",
            "explore_weight",
            "change_node_type_weight",
            "change_edge_type_weight",
            "number_of_negative_samples",
            "iterations"
        ]
        return dict(
            **{
                key: value
                for key, value in super().parameters().items()
                if key not in removed
            }
        )

    @classmethod
    def model_name(cls) -> str:
        """Returns name of the model."""
        return "DeepWalk GloVe"